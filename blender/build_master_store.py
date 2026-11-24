"""
Master 3D Supermarket Scene Generator.
Correct orientation:
Aisles run along Y (from Y = -8.0 to Y = 8.0, length = 16.0m).
Shelf width is X: shelves face customers walking north-south down aisles!
Products are placed with explicit absolute coordinates (x, y, z) on each shelf tier without transform_apply clearing location!
"""

import bpy
import math

def build_master_supermarket():
    print("[StoreBuilder] Cleaning entire scene...")
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    for block in [bpy.data.meshes, bpy.data.materials, bpy.data.lights, bpy.data.cameras]:
        for item in block:
            block.remove(item)

    # 1. PBR MATERIALS
    mats = {}
    def create_mat(name, color, roughness=0.4, metallic=0.0, emission=None, emission_strength=1.0):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            if "Base Color" in bsdf.inputs:
                bsdf.inputs["Base Color"].default_value = color
            if "Roughness" in bsdf.inputs:
                bsdf.inputs["Roughness"].default_value = roughness
            if "Metallic" in bsdf.inputs:
                bsdf.inputs["Metallic"].default_value = metallic
            if emission:
                if "Emission Color" in bsdf.inputs:
                    bsdf.inputs["Emission Color"].default_value = emission
                elif "Emission" in bsdf.inputs:
                    bsdf.inputs["Emission"].default_value = emission
                if "Emission Strength" in bsdf.inputs:
                    bsdf.inputs["Emission Strength"].default_value = emission_strength
        return mat

    # Checker tile floor
    floor_mat = bpy.data.materials.new(name="Mat_Floor_Tile")
    floor_mat.use_nodes = True
    nodes = floor_mat.node_tree.nodes
    nodes.clear()
    tex_coord = nodes.new('ShaderNodeTexCoord')
    mapping = nodes.new('ShaderNodeMapping')
    mapping.inputs['Scale'].default_value = (38.0, 44.0, 1.0)
    checker = nodes.new('ShaderNodeTexChecker')
    checker.inputs['Color1'].default_value = (0.95, 0.96, 0.98, 1.0)
    checker.inputs['Color2'].default_value = (0.84, 0.86, 0.90, 1.0)
    checker.inputs['Scale'].default_value = 1.0
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Roughness'].default_value = 0.15
    out = nodes.new('ShaderNodeOutputMaterial')
    links = floor_mat.node_tree.links
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], checker.inputs['Vector'])
    links.new(checker.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(bsdf.outputs[0], out.inputs[0])
    mats['floor'] = floor_mat

    mats['wall'] = create_mat("Mat_Wall", (0.93, 0.94, 0.96, 1.0), roughness=0.6)
    mats['wall_blue'] = create_mat("Mat_Wall_Blue", (0.05, 0.35, 0.75, 1.0), roughness=0.3)
    mats['metal_shelf'] = create_mat("Mat_Shelf_Metal", (0.90, 0.92, 0.94, 1.0), roughness=0.25, metallic=0.7)
    mats['metal_dark'] = create_mat("Mat_Metal_Dark", (0.15, 0.16, 0.18, 1.0), roughness=0.35, metallic=0.9)
    mats['metal_chrome'] = create_mat("Mat_Chrome", (0.95, 0.95, 0.97, 1.0), roughness=0.08, metallic=0.98)
    mats['price_strip'] = create_mat("Mat_Price_Strip", (0.95, 0.15, 0.15, 1.0), roughness=0.2)
    mats['glass'] = create_mat("Mat_Glass", (0.9, 0.96, 1.0, 1.0), roughness=0.05)
    mats['conveyor'] = create_mat("Mat_Conveyor", (0.08, 0.08, 0.09, 1.0), roughness=0.7)
    mats['screen'] = create_mat("Mat_POS_Screen", (0.05, 0.05, 0.08, 1.0), emission=(0.1, 0.75, 1.0, 1.0), emission_strength=3.0)
    mats['light'] = create_mat("Mat_Ceiling_Light", (1.0, 1.0, 1.0, 1.0), emission=(1.0, 0.98, 0.92, 1.0), emission_strength=5.0)

    # Category signage
    mats['sign_food'] = create_mat("Mat_Sign_Food", (0.12, 0.65, 0.22, 1.0), roughness=0.2)
    mats['sign_dairy'] = create_mat("Mat_Sign_Dairy", (0.15, 0.55, 0.85, 1.0), roughness=0.2)
    mats['sign_pantry'] = create_mat("Mat_Sign_Pantry", (0.85, 0.45, 0.12, 1.0), roughness=0.2)
    mats['sign_hazard'] = create_mat("Mat_Sign_Hazard", (0.90, 0.20, 0.10, 1.0), roughness=0.2)
    mats['sign_elec'] = create_mat("Mat_Sign_Elec", (0.10, 0.35, 0.82, 1.0), roughness=0.2)
    mats['sign_cloth'] = create_mat("Mat_Sign_Cloth", (0.65, 0.20, 0.60, 1.0), roughness=0.2)

    # Waste stations
    mats['zone_donation'] = create_mat("Mat_Zone_Donation", (0.12, 0.72, 0.28, 1.0), roughness=0.3)
    mats['zone_recycling'] = create_mat("Mat_Zone_Recycling", (0.08, 0.48, 0.92, 1.0), roughness=0.3)
    mats['zone_organic'] = create_mat("Mat_Zone_Organic", (0.78, 0.52, 0.12, 1.0), roughness=0.4)
    mats['zone_hazardous'] = create_mat("Mat_Zone_Hazardous", (0.90, 0.12, 0.12, 1.0), roughness=0.3)
    mats['hazard_stripe'] = create_mat("Mat_Hazard_Stripe", (0.98, 0.82, 0.02, 1.0), roughness=0.25)

    # Products
    mats['prod_apple'] = create_mat("Mat_Prod_Apple", (0.88, 0.08, 0.08, 1.0), roughness=0.2)
    mats['prod_orange'] = create_mat("Mat_Prod_Orange", (0.98, 0.45, 0.05, 1.0), roughness=0.35)
    mats['prod_banana'] = create_mat("Mat_Prod_Banana", (0.98, 0.85, 0.12, 1.0), roughness=0.3)
    mats['prod_tomato'] = create_mat("Mat_Prod_Tomato", (0.92, 0.12, 0.10, 1.0), roughness=0.15)
    mats['prod_milk'] = create_mat("Mat_Prod_Milk", (0.95, 0.96, 0.98, 1.0), roughness=0.25)
    mats['prod_juice'] = create_mat("Mat_Prod_Juice", (0.95, 0.42, 0.08, 1.0), roughness=0.15)
    mats['prod_cereal'] = create_mat("Mat_Prod_Cereal", (0.88, 0.40, 0.15, 1.0), roughness=0.45)
    mats['prod_bread'] = create_mat("Mat_Prod_Bread", (0.82, 0.58, 0.32, 1.0), roughness=0.6)
    mats['prod_phone'] = create_mat("Mat_Prod_Phone", (0.12, 0.13, 0.15, 1.0), roughness=0.08, metallic=0.92)
    mats['prod_laptop'] = create_mat("Mat_Prod_Laptop", (0.75, 0.76, 0.78, 1.0), roughness=0.18, metallic=0.88)
    mats['prod_headphone'] = create_mat("Mat_Prod_Headphone", (0.15, 0.15, 0.18, 1.0), roughness=0.25, metallic=0.6)
    mats['prod_battery'] = create_mat("Mat_Prod_Battery", (0.95, 0.75, 0.05, 1.0), roughness=0.25, metallic=0.7)
    mats['prod_shirt_blue'] = create_mat("Mat_Prod_ShirtBlue", (0.18, 0.42, 0.72, 1.0), roughness=0.85)
    mats['prod_shirt_red'] = create_mat("Mat_Prod_ShirtRed", (0.75, 0.18, 0.22, 1.0), roughness=0.85)
    mats['prod_trousers'] = create_mat("Mat_Prod_Trousers", (0.15, 0.18, 0.24, 1.0), roughness=0.8)
    mats['prod_shoebox'] = create_mat("Mat_Prod_ShoeBox", (0.85, 0.45, 0.20, 1.0), roughness=0.4)
    mats['prod_chem_bottle'] = create_mat("Mat_Prod_ChemBottle", (0.92, 0.15, 0.15, 1.0), roughness=0.25)
    mats['prod_chem_spray'] = create_mat("Mat_Prod_ChemSpray", (0.95, 0.85, 0.05, 1.0), roughness=0.25)

    # Master Collection
    master_col = bpy.data.collections.new("Retail_Simulator_Master")
    bpy.context.scene.collection.children.link(master_col)

    def add_box(name, size, location, material, col=master_col):
        sx, sy, sz = size
        mesh = bpy.data.meshes.new(name + "_Mesh")
        obj = bpy.data.objects.new(name, mesh)
        verts = [
            (-sx/2, -sy/2, 0), (sx/2, -sy/2, 0), (sx/2, sy/2, 0), (-sx/2, sy/2, 0),
            (-sx/2, -sy/2, sz), (sx/2, -sy/2, sz), (sx/2, sy/2, sz), (-sx/2, sy/2, sz)
        ]
        faces = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
        mesh.from_pydata(verts, [], faces)
        mesh.update()
        obj.location = location
        if material:
            obj.data.materials.append(material)
        col.objects.link(obj)
        return obj

    # 2. ARCHITECTURE
    arch_col = bpy.data.collections.new("01_Architecture")
    master_col.children.link(arch_col)
    add_box("Floor", (38.0, 44.0, 0.2), (0.0, 0.0, -0.2), mats['floor'], arch_col)
    add_box("Wall_N", (38.0, 0.4, 6.0), (0.0, 22.0, 0.0), mats['wall'], arch_col)
    add_box("Wall_N_Stripe", (38.0, 0.42, 0.5), (0.0, 22.0, 4.2), mats['wall_blue'], arch_col)
    add_box("Wall_E", (0.4, 44.0, 6.0), (19.0, 0.0, 0.0), mats['wall'], arch_col)
    add_box("Wall_E_Stripe", (0.42, 44.0, 0.5), (19.0, 0.0, 4.2), mats['wall_blue'], arch_col)
    add_box("Wall_W", (0.4, 44.0, 6.0), (-19.0, 0.0, 0.0), mats['wall'], arch_col)
    add_box("Wall_W_Stripe", (0.42, 44.0, 0.5), (-19.0, 0.0, 4.2), mats['wall_blue'], arch_col)
    add_box("Wall_S_L", (14.0, 0.4, 6.0), (-12.0, -22.0, 0.0), mats['wall'], arch_col)
    add_box("Wall_S_R", (14.0, 0.4, 6.0), (12.0, -22.0, 0.0), mats['wall'], arch_col)
    add_box("Wall_S_Header", (10.0, 0.4, 2.2), (0.0, -22.0, 3.8), mats['wall_blue'], arch_col)
    add_box("Door_L", (4.5, 0.08, 3.7), (-2.4, -22.0, 0.0), mats['glass'], arch_col)
    add_box("Door_R", (4.5, 0.08, 3.7), (2.4, -22.0, 0.0), mats['glass'], arch_col)
    add_box("Store_Sign_Ext", (12.0, 0.3, 1.4), (0.0, -22.2, 4.4), mats['wall_blue'], arch_col)
    add_box("Partition_L", (16.0, 0.3, 4.5), (-11.0, 13.0, 0.0), mats['wall'], arch_col)
    add_box("Partition_R", (16.0, 0.3, 4.5), (11.0, 13.0, 0.0), mats['wall'], arch_col)

    # 3. LIGHTING
    light_col = bpy.data.collections.new("02_Lighting")
    master_col.children.link(light_col)
    for lx in [-12.0, -6.0, 0.0, 6.0, 12.0]:
        for ly in [-14.0, -7.0, 0.0, 7.0, 16.0]:
            add_box(f"Luminaire_{lx}_{ly}", (2.8, 0.4, 0.15), (lx, ly, 5.7), mats['light'], light_col)
            ldata = bpy.data.lights.new(name=f"LData_{lx}_{ly}", type='AREA')
            ldata.energy = 420.0
            ldata.size = 2.4
            ldata.size_y = 0.4
            ldata.color = (1.0, 0.98, 0.95)
            lobj = bpy.data.objects.new(name=f"Light_{lx}_{ly}", object_data=ldata)
            lobj.location = (lx, ly, 5.6)
            light_col.objects.link(lobj)

    sdata = bpy.data.lights.new(name="SunFill", type='SUN')
    sdata.energy = 2.8
    sobj = bpy.data.objects.new(name="SunObj", object_data=sdata)
    sobj.location = (10.0, -10.0, 20.0)
    sobj.rotation_euler = (math.radians(35), math.radians(20), math.radians(-30))
    light_col.objects.link(sobj)

    # 4. GONDOLA SHELVES & DENSE PRODUCTS
    # 6 Aisles spaced along X: -12.5, -7.5, -2.5, 2.5, 7.5, 12.5
    # Each aisle gondola runs North-South along Y from Y = -11.0 to Y = 9.0 (Length = 20.0m)
    # Gondola has Left Face (-X) and Right Face (+X), depth X = 1.0m
    aisles_col = bpy.data.collections.new("03_Supermarket_Aisles")
    master_col.children.link(aisles_col)
    prods_col = bpy.data.collections.new("04_Supermarket_Products")
    master_col.children.link(prods_col)

    aisle_cfgs = [
        {"id": 1, "x": -12.5, "cat": "PRODUCE", "name": "Fresh Produce", "sign": mats['sign_food']},
        {"id": 2, "x": -7.5,  "cat": "DAIRY",   "name": "Dairy & Beverages", "sign": mats['sign_dairy']},
        {"id": 3, "x": -2.5,  "cat": "PANTRY",  "name": "Pantry & Bakery", "sign": mats['sign_pantry']},
        {"id": 4, "x": 2.5,   "cat": "HAZARD",  "name": "Household & Chemicals", "sign": mats['sign_hazard']},
        {"id": 5, "x": 7.5,   "cat": "ELEC",    "name": "Consumer Tech", "sign": mats['sign_elec']},
        {"id": 6, "x": 12.5,  "cat": "CLOTH",   "name": "Apparel & Shoes", "sign": mats['sign_cloth']}
    ]

    tier_z_levels = [0.4, 0.9, 1.4, 1.9]
    gondola_length = 18.0 # From Y = -9.0 to Y = 9.0
    gondola_depth = 1.1   # X dimension

    # Product spawning primitives
    def add_product_mesh(name, loc, primitive_type, size, material):
        mesh = bpy.data.meshes.new(name + "_Mesh")
        obj = bpy.data.objects.new(name, mesh)
        
        if primitive_type == "CUBE":
            sx, sy, sz = size
            verts = [
                (-sx/2, -sy/2, 0), (sx/2, -sy/2, 0), (sx/2, sy/2, 0), (-sx/2, sy/2, 0),
                (-sx/2, -sy/2, sz), (sx/2, -sy/2, sz), (sx/2, sy/2, sz), (-sx/2, sy/2, sz)
            ]
            faces = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
            mesh.from_pydata(verts, [], faces)
        elif primitive_type == "SPHERE":
            r = size[0]
            # Procedural UV Sphere
            verts = []
            faces = []
            rings = 8
            segs = 12
            for i in range(rings + 1):
                theta = i * math.pi / rings
                sin_t = math.sin(theta)
                cos_t = math.cos(theta)
                for j in range(segs):
                    phi = j * 2 * math.pi / segs
                    verts.append((r * sin_t * math.cos(phi), r * sin_t * math.sin(phi), r * (cos_t + 1.0)))
            for i in range(rings):
                for j in range(segs):
                    p1 = i * segs + j
                    p2 = i * segs + (j + 1) % segs
                    p3 = (i + 1) * segs + (j + 1) % segs
                    p4 = (i + 1) * segs + j
                    faces.append((p1, p2, p3, p4))
            mesh.from_pydata(verts, [], faces)
        elif primitive_type == "CYLINDER":
            r = size[0]
            h = size[1]
            verts = []
            faces = []
            segs = 12
            for j in range(segs):
                phi = j * 2 * math.pi / segs
                verts.append((r * math.cos(phi), r * math.sin(phi), 0))
            for j in range(segs):
                phi = j * 2 * math.pi / segs
                verts.append((r * math.cos(phi), r * math.sin(phi), h))
            for j in range(segs):
                p1 = j
                p2 = (j + 1) % segs
                p3 = (j + 1) % segs + segs
                p4 = j + segs
                faces.append((p1, p2, p3, p4))
            mesh.from_pydata(verts, [], faces)

        mesh.update()
        obj.location = loc
        if material:
            obj.data.materials.append(material)
        prods_col.objects.link(obj)
        return obj

    for cfg in aisle_cfgs:
        a_id = cfg['id']
        ax = cfg['x']
        cat = cfg['cat']
        acol = bpy.data.collections.new(f"Aisle_{a_id}")
        aisles_col.children.link(acol)

        # 1. Continuous Double-sided Gondola Shelving Structure along Y
        add_box(f"Aisle_{a_id}_Gondola_Base", (gondola_depth, gondola_length, 0.15), (ax, 0.0, 0.0), mats['metal_shelf'], acol)
        add_box(f"Aisle_{a_id}_Center_Backpanel", (0.05, gondola_length, 2.3), (ax, 0.0, 0.1), mats['metal_dark'], acol)
        
        # Endcap Posts & Displays
        add_box(f"Aisle_{a_id}_Endcap_South", (gondola_depth + 0.1, 0.1, 2.4), (ax, -gondola_length/2, 0.0), mats['metal_dark'], acol)
        add_box(f"Aisle_{a_id}_Endcap_North", (gondola_depth + 0.1, 0.1, 2.4), (ax, gondola_length/2, 0.0), mats['metal_dark'], acol)

        # 4 Shelf levels on West side (-X) and East side (+X)
        for tidx, tz in enumerate(tier_z_levels):
            # West shelf ledge
            add_box(f"Aisle_{a_id}_TierW_{tidx+1}", (0.45, gondola_length - 0.1, 0.04), (ax - 0.25, 0.0, tz), mats['metal_shelf'], acol)
            add_box(f"Aisle_{a_id}_PriceStripW_{tidx+1}", (0.02, gondola_length - 0.1, 0.04), (ax - 0.48, 0.0, tz + 0.02), mats['price_strip'], acol)
            # East shelf ledge
            add_box(f"Aisle_{a_id}_TierE_{tidx+1}", (0.45, gondola_length - 0.1, 0.04), (ax + 0.25, 0.0, tz), mats['metal_shelf'], acol)
            add_box(f"Aisle_{a_id}_PriceStripE_{tidx+1}", (0.02, gondola_length - 0.1, 0.04), (ax + 0.48, 0.0, tz + 0.02), mats['price_strip'], acol)

        # Overhead category signboard suspended from ceiling
        add_box(f"Sign_Aisle_{a_id}", (0.1, 3.2, 0.8), (ax, 0.0, 3.5), cfg['sign'], acol)
        add_box(f"Sign_Cable1_{a_id}", (0.02, 0.02, 2.2), (ax, -1.3, 3.5), mats['metal_chrome'], acol)
        add_box(f"Sign_Cable2_{a_id}", (0.02, 0.02, 2.2), (ax, 1.3, 3.5), mats['metal_chrome'], acol)

        # 2. POPULATE EVERY SINGLE TIER WITH DENSE ITEMS ALONG Y
        # 10 product slots along the 18m length of the aisle!
        y_positions = [-7.5, -5.8, -4.2, -2.5, -0.9, 0.8, 2.4, 4.1, 5.7, 7.4]

        for t_idx, tz in enumerate(tier_z_levels[:3]): # Tiers 1, 2, 3
            for slot_i, py in enumerate(y_positions):
                # Populate both West Face (-X) and East Face (+X)
                for side, x_off in [("W", -0.28), ("E", 0.28)]:
                    ploc = (ax + x_off, py, tz + 0.04)
                    pname = f"A{a_id}_{side}_T{t_idx+1}_S{slot_i+1}"

                    if cat == "PRODUCE":
                        if t_idx == 0:
                            add_product_mesh(f"{pname}_Apple", ploc, "SPHERE", (0.09, 0.09, 0.09), mats['prod_apple'])
                        elif t_idx == 1:
                            if slot_i % 2 == 0:
                                add_product_mesh(f"{pname}_Orange", ploc, "SPHERE", (0.095, 0.095, 0.095), mats['prod_orange'])
                            else:
                                add_product_mesh(f"{pname}_Tomato", ploc, "SPHERE", (0.085, 0.085, 0.085), mats['prod_tomato'])
                        else:
                            add_product_mesh(f"{pname}_Banana", ploc, "CYLINDER", (0.04, 0.24), mats['prod_banana'])

                    elif cat == "DAIRY":
                        if t_idx == 0 or slot_i % 2 == 0:
                            add_product_mesh(f"{pname}_Milk", ploc, "CUBE", (0.13, 0.13, 0.28), mats['prod_milk'])
                        else:
                            add_product_mesh(f"{pname}_Juice", ploc, "CYLINDER", (0.06, 0.26), mats['prod_juice'])

                    elif cat == "PANTRY":
                        if t_idx == 0:
                            add_product_mesh(f"{pname}_Bread", ploc, "CUBE", (0.14, 0.26, 0.14), mats['prod_bread'])
                        else:
                            add_product_mesh(f"{pname}_Cereal", ploc, "CUBE", (0.10, 0.22, 0.34), mats['prod_cereal'])

                    elif cat == "HAZARD":
                        if slot_i % 2 == 0:
                            add_product_mesh(f"{pname}_Bleach", ploc, "CYLINDER", (0.07, 0.30), mats['prod_chem_bottle'])
                        else:
                            add_product_mesh(f"{pname}_Spray", ploc, "CYLINDER", (0.055, 0.24), mats['prod_chem_spray'])

                    elif cat == "ELEC":
                        if t_idx == 0:
                            add_product_mesh(f"{pname}_Phone", ploc, "CUBE", (0.03, 0.18, 0.10), mats['prod_phone'])
                        elif t_idx == 1:
                            add_product_mesh(f"{pname}_Headphone", ploc, "CYLINDER", (0.09, 0.06), mats['prod_headphone'])
                        elif t_idx == 2 and slot_i < 6:
                            add_product_mesh(f"{pname}_Laptop", ploc, "CUBE", (0.24, 0.32, 0.03), mats['prod_laptop'])
                        else:
                            add_product_mesh(f"{pname}_Battery", ploc, "CUBE", (0.04, 0.14, 0.16), mats['prod_battery'])

                    elif cat == "CLOTH":
                        if t_idx == 0:
                            cmat = mats['prod_shirt_blue'] if slot_i % 2 == 0 else mats['prod_shirt_red']
                            add_product_mesh(f"{pname}_Shirt", ploc, "CUBE", (0.28, 0.26, 0.09), cmat)
                        elif t_idx == 1:
                            add_product_mesh(f"{pname}_Trousers", ploc, "CUBE", (0.26, 0.28, 0.11), mats['prod_trousers'])
                        else:
                            add_product_mesh(f"{pname}_ShoeBox", ploc, "CUBE", (0.24, 0.32, 0.15), mats['prod_shoebox'])

    # 5. FRONT CHECKOUT DESKS, CARTS & PROPS
    chk_col = bpy.data.collections.new("05_Checkout_Counters")
    master_col.children.link(chk_col)
    for i, cx in enumerate([-9.0, -3.0, 3.0, 9.0]):
        prefix = f"Checkout_{i+1}"
        add_box(f"{prefix}_Base", (2.4, 3.2, 0.95), (cx, -16.0, 0.0), mats['wall_blue'], chk_col)
        add_box(f"{prefix}_Belt", (0.6, 2.2, 0.05), (cx, -16.0, 0.95), mats['conveyor'], chk_col)
        add_box(f"{prefix}_Stand", (0.08, 0.08, 0.35), (cx + 0.5, -15.0, 0.95), mats['metal_dark'], chk_col)
        scr = add_box(f"{prefix}_Screen", (0.35, 0.05, 0.28), (cx + 0.5, -15.0, 1.3), mats['screen'], chk_col)
        scr.rotation_euler.x = math.radians(-15)

    add_box("Cart_Rail_1", (0.08, 6.0, 0.9), (-15.5, -17.0, 0.0), mats['metal_chrome'], chk_col)
    add_box("Cart_Rail_2", (0.08, 6.0, 0.9), (-17.0, -17.0, 0.0), mats['metal_chrome'], chk_col)
    for c_i in range(5):
        cy = -19.5 + c_i * 1.0
        add_box(f"Cart_{c_i+1}_Basket", (0.6, 0.85, 0.5), (-16.25, cy, 0.45), mats['metal_chrome'], chk_col)
        add_box(f"Cart_{c_i+1}_Handle", (0.65, 0.05, 0.05), (-16.25, cy + 0.42, 0.95), mats['wall_blue'], chk_col)

    for b_i in range(6):
        add_box(f"Basket_Stack_{b_i+1}", (0.45, 0.35, 0.08), (-13.5, -20.5, b_i * 0.09), mats['sign_food'], chk_col)

    # 6. BACKROOM STORAGE & RESTOCK CONVEYOR
    stor_col = bpy.data.collections.new("06_Storage_Conveyor")
    master_col.children.link(stor_col)
    for px in [-12.0, -4.0, 4.0, 12.0]:
        add_box(f"Pallet_Rack_{px}", (6.5, 1.8, 4.8), (px, 18.5, 0.0), mats['metal_dark'], stor_col)
    add_box("Conveyor_Frame", (1.25, 10.0, 0.85), (0.0, 15.5, 0.0), mats['metal_dark'], stor_col)
    add_box("Conveyor_Surface", (1.1, 9.8, 0.05), (0.0, 15.5, 0.85), mats['conveyor'], stor_col)

    # 7. WASTE & OPTIMIZATION STATIONS
    waste_col = bpy.data.collections.new("07_Waste_Stations")
    master_col.children.link(waste_col)
    stations = [
        ("Donation", 8.0, mats['zone_donation']),
        ("Recycling", 3.0, mats['zone_recycling']),
        ("Organic", -2.0, mats['zone_organic']),
        ("Hazardous", -7.0, mats['zone_hazardous'])
    ]
    for sname, sy, smat in stations:
        add_box(f"{sname}_Pad", (4.2, 3.8, 0.03), (-15.5, sy, 0.01), smat, waste_col)
        add_box(f"{sname}_Sign", (0.1, 3.4, 0.9), (-18.7, sy, 3.2), smat, waste_col)
        if sname == "Donation":
            add_box("Donation_Hamper_1", (1.2, 1.2, 1.0), (-16.0, sy - 0.8, 0.0), smat, waste_col)
            add_box("Donation_Hamper_2", (1.2, 1.2, 1.0), (-16.0, sy + 0.8, 0.0), smat, waste_col)
        elif sname == "Recycling":
            for b_i, b_off in enumerate([-0.9, 0.0, 0.9]):
                add_box(f"Recycle_Bin_{b_i+1}", (0.9, 0.7, 1.1), (-15.8, sy + b_off, 0.0), smat, waste_col)
        elif sname == "Organic":
            add_box("Organic_Dumpster", (1.8, 2.6, 1.2), (-15.5, sy, 0.0), smat, waste_col)
        elif sname == "Hazardous":
            add_box("Hazard_Locker", (1.2, 1.8, 2.2), (-16.2, sy - 0.6, 0.0), smat, waste_col)
            add_box("Hazard_Drum", (1.0, 1.0, 1.2), (-15.0, sy + 0.9, 0.0), mats['hazard_stripe'], waste_col)

    # 8. MULTI-CAMERA SETUP
    cam_col = bpy.data.collections.new("08_Cameras")
    master_col.children.link(cam_col)

    # Position main overview camera looking down the central supermarket promenade!
    cams = [
        ("Cam_01_Supermarket_Overview", (0.0, -21.0, 5.5), (math.radians(75), 0, 0), "PERSP", 24.0),
        ("Cam_02_Food_Section", (-10.0, -14.0, 3.2), (math.radians(72), 0, math.radians(-15)), "PERSP", 32.0),
        ("Cam_03_Electronics_Clothing", (10.0, -14.0, 3.2), (math.radians(72), 0, math.radians(15)), "PERSP", 32.0),
        ("Cam_04_Storage_Conveyor", (0.0, 18.0, 6.5), (math.radians(70), 0, math.radians(180)), "PERSP", 32.0),
        ("Cam_05_Waste_Donation_Zones", (-16.0, 6.0, 5.5), (math.radians(60), 0, math.radians(-65)), "PERSP", 30.0),
        ("Cam_06_Isometric_TopView", (22.0, -22.0, 28.0), (math.radians(54.736), 0, math.radians(45)), "ORTHO", 42.0)
    ]

    for cname, cloc, crot, ctype, param in cams:
        cdata = bpy.data.cameras.new(name=cname + "_Data")
        cdata.type = ctype
        if ctype == "PERSP":
            cdata.lens = param
        else:
            cdata.ortho_scale = param
        cobj = bpy.data.objects.new(name=cname, object_data=cdata)
        cobj.location = cloc
        cobj.rotation_euler = crot
        cam_col.objects.link(cobj)
        if cname == "Cam_01_Supermarket_Overview":
            bpy.context.scene.camera = cobj

    print(f"[StoreBuilder] Complete! Total scene objects: {len(bpy.data.objects)}")

if __name__ == "__main__":
    build_master_supermarket()
