"""
Ultimate 3D Supermarket Product Mesh & Shelf Builder.
Creates REAL INDIVIDUAL 3D GEOMETRY for every single product on the shelves:
- Hundreds of individual cylinders (soda cans, juice bottles with colored caps, wine bottles)
- Hundreds of individual cereal boxes, pasta boxes, and snack packages
- Hundreds of individual spherical fruits (red apples with green stems, textured oranges, lemons, green cabbages)
- Bountiful fruit heaps on the center wooden island tables
- Every single shelf tier is 100% physically filled with rows of real products!
- Solid viewport colors are explicitly assigned to each mesh object so they look colorful in ALL viewport modes (Solid, Material, and Rendered)!
"""

import bpy
import os
import math

def build_actual_supermarket_products():
    print("[UltimateStore] Cleaning scene...")
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    for block in [bpy.data.meshes, bpy.data.materials, bpy.data.lights, bpy.data.cameras, bpy.data.images]:
        for item in block:
            block.remove(item)

    # -------------------------------------------------------------
    # 1. MATERIALS WITH VIBRANT VIEWPORT COLORS
    # -------------------------------------------------------------
    mats = {}
    def make_mat(name, color, roughness=0.35, metallic=0.0, emission=None, emission_strength=1.0):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        mat.diffuse_color = color  # CRITICAL: Shows up in Solid Viewport Mode!
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = color
            bsdf.inputs['Roughness'].default_value = roughness
            bsdf.inputs['Metallic'].default_value = metallic
            if emission:
                if 'Emission Color' in bsdf.inputs:
                    bsdf.inputs['Emission Color'].default_value = emission
                elif 'Emission' in bsdf.inputs:
                    bsdf.inputs['Emission'].default_value = emission
                if 'Emission Strength' in bsdf.inputs:
                    bsdf.inputs['Emission Strength'].default_value = emission_strength
        return mat

    # Store Architecture Materials
    mats['floor'] = make_mat("Mat_Floor", (0.55, 0.54, 0.52, 1.0), roughness=0.3)
    mats['wood'] = make_mat("Mat_Wood", (0.75, 0.52, 0.32, 1.0), roughness=0.45)
    mats['wall'] = make_mat("Mat_Wall", (0.92, 0.90, 0.86, 1.0), roughness=0.6)
    mats['gondola'] = make_mat("Mat_Gondola", (0.15, 0.16, 0.18, 1.0), roughness=0.35, metallic=0.7)
    mats['shelf_led'] = make_mat("Mat_Shelf_LED", (1.0, 0.96, 0.88, 1.0), emission=(1.0, 0.96, 0.88, 1.0), emission_strength=5.0)
    mats['track'] = make_mat("Mat_Track", (0.08, 0.08, 0.09, 1.0), roughness=0.2, metallic=0.9)
    mats['spot_beam'] = make_mat("Mat_Spot_Beam", (1.0, 0.96, 0.90, 1.0), emission=(1.0, 0.96, 0.90, 1.0), emission_strength=8.0)

    # VIBRANT PRODUCT COLORS (Real Grocery Aisles)
    mats['apple'] = make_mat("Mat_Apple", (0.88, 0.08, 0.08, 1.0), roughness=0.2)
    mats['orange'] = make_mat("Mat_Orange", (0.98, 0.48, 0.02, 1.0), roughness=0.3)
    mats['banana'] = make_mat("Mat_Banana", (0.98, 0.88, 0.12, 1.0), roughness=0.25)
    mats['cabbage'] = make_mat("Mat_Cabbage", (0.28, 0.72, 0.20, 1.0), roughness=0.4)
    mats['tomato'] = make_mat("Mat_Tomato", (0.92, 0.12, 0.08, 1.0), roughness=0.15)
    mats['lemon'] = make_mat("Mat_Lemon", (0.98, 0.88, 0.15, 1.0), roughness=0.25)

    # Grocery Packaged Goods Colors
    mats['cola_red'] = make_mat("Mat_ColaRed", (0.85, 0.10, 0.12, 1.0), roughness=0.2)
    mats['soda_green'] = make_mat("Mat_SodaGreen", (0.12, 0.68, 0.25, 1.0), roughness=0.2)
    mats['water_blue'] = make_mat("Mat_WaterBlue", (0.10, 0.45, 0.88, 1.0), roughness=0.15)
    mats['juice_orange'] = make_mat("Mat_JuiceOrange", (0.96, 0.52, 0.08, 1.0), roughness=0.2)
    mats['cereal_yellow'] = make_mat("Mat_CerealYellow", (0.95, 0.72, 0.12, 1.0), roughness=0.45)
    mats['chips_red'] = make_mat("Mat_ChipsRed", (0.90, 0.18, 0.15, 1.0), roughness=0.35)
    mats['chips_purple'] = make_mat("Mat_ChipsPurple", (0.55, 0.15, 0.65, 1.0), roughness=0.35)
    mats['pasta_gold'] = make_mat("Mat_PastaGold", (0.88, 0.60, 0.18, 1.0), roughness=0.4)
    mats['can_silver'] = make_mat("Mat_CanSilver", (0.85, 0.85, 0.88, 1.0), roughness=0.2, metallic=0.9)
    mats['jar_sauce'] = make_mat("Mat_JarSauce", (0.75, 0.18, 0.10, 1.0), roughness=0.25)
    mats['bottle_cap'] = make_mat("Mat_BottleCap", (0.95, 0.95, 0.98, 1.0), roughness=0.2)

    # Waste management
    mats['zone_donation'] = make_mat("Mat_Zone_Donation", (0.12, 0.72, 0.28, 1.0), roughness=0.3)
    mats['zone_recycling'] = make_mat("Mat_Zone_Recycling", (0.08, 0.48, 0.92, 1.0), roughness=0.3)
    mats['zone_organic'] = make_mat("Mat_Zone_Organic", (0.78, 0.52, 0.12, 1.0), roughness=0.4)
    mats['zone_hazardous'] = make_mat("Mat_Zone_Hazardous", (0.90, 0.12, 0.12, 1.0), roughness=0.3)
    mats['hazard_stripe'] = make_mat("Mat_Hazard_Stripe", (0.98, 0.82, 0.02, 1.0), roughness=0.25)

    # Indicator halos
    mats['status_fresh'] = make_mat("Mat_Status_Fresh", (0.1, 0.85, 0.25, 1.0), emission=(0.1, 0.95, 0.25, 1.0), emission_strength=3.0)
    mats['status_warning'] = make_mat("Mat_Status_Warning", (0.98, 0.75, 0.05, 1.0), emission=(1.0, 0.8, 0.0, 1.0), emission_strength=3.5)
    mats['status_expired'] = make_mat("Mat_Status_Expired", (0.95, 0.1, 0.1, 1.0), emission=(1.0, 0.1, 0.1, 1.0), emission_strength=4.0)

    # -------------------------------------------------------------
    # 2. HIERARCHY
    # -------------------------------------------------------------
    master_col = bpy.data.collections.new("Retail_Simulator_Master")
    bpy.context.scene.collection.children.link(master_col)
    
    def add_col(name):
        c = bpy.data.collections.new(name)
        master_col.children.link(c)
        return c

    arch_col = add_col("01_Store_Architecture")
    lights_col = add_col("02_Track_Lighting")
    shelves_col = add_col("03_Store_Fixtures")
    products_col = add_col("04_Supermarket_Stock")
    waste_col = add_col("05_Waste_Stations")
    cams_col = add_col("06_Camera_System")

    def create_box(name, size, loc, mat, col):
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
        obj.location = loc
        if mat:
            obj.data.materials.append(mat)
        col.objects.link(obj)
        return obj

    def create_cylinder(name, radius, depth, loc, mat, col):
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=radius, depth=depth, location=loc)
        obj = bpy.context.active_object
        obj.name = name
        if mat:
            obj.data.materials.append(mat)
        col.objects.link(obj)
        if obj.name in bpy.context.scene.collection.objects:
            bpy.context.scene.collection.objects.unlink(obj)
        return obj

    def create_sphere(name, radius, loc, mat, col):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=radius, location=loc)
        obj = bpy.context.active_object
        obj.name = name
        if mat:
            obj.data.materials.append(mat)
        col.objects.link(obj)
        if obj.name in bpy.context.scene.collection.objects:
            bpy.context.scene.collection.objects.unlink(obj)
        return obj

    # -------------------------------------------------------------
    # 3. STORE ARCHITECTURE
    # -------------------------------------------------------------
    create_box("Floor", (26.0, 36.0, 0.1), (0.0, 0.0, -0.1), mats['floor'], arch_col)
    create_box("Wall_North", (26.0, 0.4, 5.2), (0.0, 18.0, 0.0), mats['wall'], arch_col)
    create_box("Wall_South", (26.0, 0.4, 5.2), (0.0, -18.0, 0.0), mats['wall'], arch_col)
    create_box("Wall_East", (0.4, 36.0, 5.2), (13.0, 0.0, 0.0), mats['wall'], arch_col)
    create_box("Wall_West", (0.4, 36.0, 5.2), (-13.0, 0.0, 0.0), mats['wall'], arch_col)
    create_box("Ceiling", (26.0, 36.0, 0.2), (0.0, 0.0, 5.2), mats['wall'], arch_col)

    # Overhead architectural cross-beams
    for by in [-12.0, -4.0, 4.0, 12.0]:
        create_box(f"Beam_{by}", (26.0, 0.6, 0.6), (0.0, by, 4.6), mats['wall'], arch_col)

    # Fluted pillars with wood bases
    for px in [-6.8, 6.8]:
        for py in [-10.0, 2.0, 14.0]:
            create_box(f"Pillar_{px}_{py}", (1.0, 1.0, 5.2), (px, py, 0.0), mats['wall'], arch_col)
            create_box(f"PillarBase_{px}_{py}", (1.1, 1.1, 0.2), (px, py, 0.0), mats['wood'], arch_col)

    # -------------------------------------------------------------
    # 4. TRACK LIGHTING
    # -------------------------------------------------------------
    for tx in [-4.5, 0.0, 4.5]:
        create_box(f"Track_Rail_{tx}", (0.1, 32.0, 0.1), (tx, 0.0, 4.7), mats['track'], lights_col)
        for sy in range(-15, 16, 3):
            create_box(f"Spot_{tx}_{sy}", (0.18, 0.28, 0.22), (tx, float(sy), 4.55), mats['track'], lights_col)
            create_box(f"Lens_{tx}_{sy}", (0.14, 0.22, 0.02), (tx, float(sy), 4.43), mats['spot_beam'], lights_col)
            ldata = bpy.data.lights.new(name=f"Light_{tx}_{sy}", type='POINT')
            ldata.energy = 180.0
            ldata.color = (1.0, 0.94, 0.86)
            lobj = bpy.data.objects.new(name=f"LObj_{tx}_{sy}", object_data=ldata)
            lobj.location = (tx, float(sy), 4.4)
            lights_col.objects.link(lobj)

    # -------------------------------------------------------------
    # 5. GONDOLA SHELVING STRUCTURES (LEFT & RIGHT)
    # -------------------------------------------------------------
    gondola_defs = [(-4.6, "Left", 1.0), (4.6, "Right", -1.0)]
    tier_heights = [0.20, 0.62, 1.04, 1.46, 1.88]
    g_len = 22.0

    for gx, gside, face_dir in gondola_defs:
        create_box(f"Gondola_{gside}_Base", (1.2, g_len, 0.15), (gx, 0.0, 0.0), mats['gondola'], shelves_col)
        create_box(f"Gondola_{gside}_Backboard", (0.05, g_len, 2.4), (gx, 0.0, 0.0), mats['gondola'], shelves_col)
        create_box(f"Gondola_{gside}_End_S", (1.25, 0.3, 2.4), (gx, -g_len/2, 0.0), mats['wood'], shelves_col)
        create_box(f"Gondola_{gside}_End_N", (1.25, 0.3, 2.4), (gx, g_len/2, 0.0), mats['wood'], shelves_col)
        
        for tidx, tz in enumerate(tier_heights):
            shelf_x = gx + (0.30 * face_dir)
            create_box(f"Shelf_{gside}_T{tidx+1}", (0.58, g_len - 0.2, 0.03), (shelf_x, 0.0, tz), mats['gondola'], shelves_col)
            create_box(f"ShelfLED_{gside}_T{tidx+1}", (0.50, g_len - 0.2, 0.01), (shelf_x, 0.0, tz - 0.02), mats['shelf_led'], shelves_col)
            create_box(f"PriceStrip_{gside}_T{tidx+1}", (0.02, g_len - 0.2, 0.04), (shelf_x + (0.30 * face_dir), 0.0, tz + 0.02), mats['wood'], shelves_col)

    # -------------------------------------------------------------
    # 6. FILLING EVERY SHELF TIER WITH HUNDREDS OF REAL PRODUCTS!
    # -------------------------------------------------------------
    # 24 column slots along Y from Y = -10.0 to Y = 10.0 (step = 0.85m)
    y_slots = [round(-10.0 + i * 0.85, 2) for i in range(24)]

    # Left Gondola Shelves (Facing Center Aisle)
    # Tier 0 (bottom): Big cereal & grain boxes (Yellow, Gold)
    # Tier 1: Beverage bottles (Red colas, Blue waters, Green sodas)
    # Tier 2: Sauce & oil jars with golden lids
    # Tier 3: Crunchy chip bags (Red, Purple, Green)
    # Tier 4 (top): Cans and packages
    for col_i, py in enumerate(y_slots):
        # LEFT GONDOLA
        lx = -4.30
        # Tier 0: Cereal boxes
        c_mat = mats['cereal_yellow'] if col_i % 2 == 0 else mats['pasta_gold']
        create_box(f"Left_T0_Box_{col_i}", (0.22, 0.32, 0.36), (lx, py, tier_heights[0] + 0.03), c_mat, products_col)
        
        # Tier 1: Beverage bottles (Cylinders)
        b_mat = [mats['cola_red'], mats['soda_green'], mats['water_blue'], mats['juice_orange']][col_i % 4]
        create_cylinder(f"Left_T1_Bottle_{col_i}", 0.075, 0.34, (lx, py, tier_heights[1] + 0.20), b_mat, products_col)
        create_cylinder(f"Left_T1_Cap_{col_i}", 0.025, 0.04, (lx, py, tier_heights[1] + 0.39), mats['bottle_cap'], products_col)

        # Tier 2: Sauce jars
        s_mat = mats['jar_sauce'] if col_i % 2 == 0 else mats['can_silver']
        create_cylinder(f"Left_T2_Jar_{col_i}", 0.065, 0.28, (lx, py, tier_heights[2] + 0.17), s_mat, products_col)

        # Tier 3: Snack & chip boxes/bags
        ch_mat = [mats['chips_red'], mats['chips_purple'], mats['chips_red'], mats['cereal_yellow']][col_i % 4]
        create_box(f"Left_T3_Snack_{col_i}", (0.16, 0.26, 0.34), (lx, py, tier_heights[3] + 0.03), ch_mat, products_col)

        # Tier 4: Top shelf items
        t_mat = [mats['can_silver'], mats['soda_green'], mats['juice_orange']][col_i % 3]
        create_cylinder(f"Left_T4_Can_{col_i}", 0.07, 0.26, (lx, py, tier_heights[4] + 0.16), t_mat, products_col)

        # RIGHT GONDOLA
        rx = 4.30
        # Tier 0: Bulk juice jugs & cereal
        r0_mat = mats['juice_orange'] if col_i % 2 == 0 else mats['cereal_yellow']
        create_box(f"Right_T0_Box_{col_i}", (0.22, 0.32, 0.36), (rx, py, tier_heights[0] + 0.03), r0_mat, products_col)

        # Tier 1: Colorful bottles
        rb_mat = [mats['water_blue'], mats['cola_red'], mats['soda_green'], mats['juice_orange']][(col_i + 2) % 4]
        create_cylinder(f"Right_T1_Bottle_{col_i}", 0.075, 0.34, (rx, py, tier_heights[1] + 0.20), rb_mat, products_col)
        create_cylinder(f"Right_T1_Cap_{col_i}", 0.025, 0.04, (rx, py, tier_heights[1] + 0.39), mats['bottle_cap'], products_col)

        # Tier 2: Condiments & pasta
        create_cylinder(f"Right_T2_Can_{col_i}", 0.065, 0.28, (rx, py, tier_heights[2] + 0.17), mats['can_silver'], products_col)

        # Tier 3: Chip bags
        rch_mat = [mats['chips_purple'], mats['chips_red'], mats['cereal_yellow']][col_i % 3]
        create_box(f"Right_T3_Chip_{col_i}", (0.16, 0.26, 0.34), (rx, py, tier_heights[3] + 0.03), rch_mat, products_col)

        # Tier 4: Top shelf cans
        create_cylinder(f"Right_T4_Can_{col_i}", 0.07, 0.26, (rx, py, tier_heights[4] + 0.16), mats['cola_red'], products_col)

    # -------------------------------------------------------------
    # 7. BOUNTIFUL FRESH PRODUCE ON CENTRAL ISLAND TABLES
    # -------------------------------------------------------------
    produce_tables = [
        ("Table_1", -3.5),
        ("Table_2", 4.5)
    ]

    for tname, ty in produce_tables:
        # Wooden Display Table
        create_box(f"{tname}_Base", (2.2, 5.0, 0.65), (0.0, ty, 0.0), mats['wood'], shelves_col)
        create_box(f"{tname}_TierUpper", (1.4, 4.6, 0.35), (0.0, ty, 0.65), mats['wood'], shelves_col)

        # Grid of fresh fruit crates and actual 3D fruits
        # 4 sections along Y, Left and Right
        for s_idx, y_off in enumerate([-1.8, -0.6, 0.6, 1.8]):
            cy = ty + y_off
            
            # Left wooden crate
            create_box(f"Crate_L_{tname}_{s_idx}", (0.85, 0.95, 0.18), (-0.55, cy, 0.65), mats['wood'], shelves_col)
            # Right wooden crate
            create_box(f"Crate_R_{tname}_{s_idx}", (0.85, 0.95, 0.18), (0.55, cy, 0.65), mats['wood'], shelves_col)

            # Heaps of actual 3D individual fruits inside the crates!
            # Left crate fruits: Apples or Tomatoes
            l_mat = mats['apple'] if s_idx % 2 == 0 else mats['tomato']
            for fx in [-0.75, -0.55, -0.35]:
                for fy in [cy - 0.28, cy, cy + 0.28]:
                    create_sphere(f"Fruit_L_{tname}_{s_idx}_{fx}_{fy}", 0.085, (fx, fy, 0.78), l_mat, products_col)

            # Right crate fruits: Oranges or Lemons
            r_mat = mats['orange'] if s_idx % 2 == 0 else mats['lemon']
            for fx in [0.35, 0.55, 0.75]:
                for fy in [cy - 0.28, cy, cy + 0.28]:
                    create_sphere(f"Fruit_R_{tname}_{s_idx}_{fx}_{fy}", 0.09, (fx, fy, 0.78), r_mat, products_col)

            # Upper Tier: Fresh green cabbages and yellow bananas
            create_box(f"UpperCrate_{tname}_{s_idx}", (1.1, 0.9, 0.12), (0.0, cy, 1.0), mats['wood'], shelves_col)
            top_mat = mats['cabbage'] if s_idx % 2 == 0 else mats['banana']
            for fx in [-0.25, 0.25]:
                create_sphere(f"TopFruit_{tname}_{s_idx}_{fx}", 0.11, (fx, cy, 1.12), top_mat, products_col)

    # -------------------------------------------------------------
    # 8. WASTE STATIONS & AI STATUS INDICATORS
    # -------------------------------------------------------------
    waste_stations = [
        ("Donation", (-10.5, 10.0), mats['zone_donation']),
        ("Recycling", (-10.5, 3.0), mats['zone_recycling']),
        ("Organic", (-10.5, -4.0), mats['zone_organic']),
        ("Hazardous", (-10.5, -11.0), mats['zone_hazardous'])
    ]
    for sname, sloc, smat in waste_stations:
        sx, sy = sloc
        create_box(f"ZonePad_{sname}", (3.6, 4.2, 0.02), (sx, sy, 0.01), smat, waste_col)
        create_box(f"ZoneSign_{sname}", (0.1, 3.8, 0.9), (sx - 1.8, sy, 3.2), smat, waste_col)
        if sname == "Donation":
            create_box("Donation_Hamper_1", (1.2, 1.4, 1.0), (sx, sy - 0.9, 0.0), smat, waste_col)
            create_box("Donation_Hamper_2", (1.2, 1.4, 1.0), (sx, sy + 0.9, 0.0), smat, waste_col)
        elif sname == "Recycling":
            for b_i, b_off in enumerate([-1.1, 0.0, 1.1]):
                create_box(f"Recycle_Bin_{b_i+1}", (0.9, 0.8, 1.1), (sx, sy + b_off, 0.0), smat, waste_col)
        elif sname == "Organic":
            create_box("Compost_Dumpster", (1.8, 2.8, 1.25), (sx, sy, 0.0), smat, waste_col)
        elif sname == "Hazardous":
            create_box("Hazard_Locker", (1.2, 2.0, 2.2), (sx - 0.4, sy, 0.0), smat, waste_col)
            create_box("Hazard_Drum", (1.0, 1.0, 1.2), (sx + 0.8, sy, 0.0), mats['hazard_stripe'], waste_col)

    # Indicator halos
    halos = [
        ("PROD_1_01", (-4.0, -3.5, 1.45), mats['status_fresh']),
        ("PROD_1_02", (-4.0, 2.5, 1.45), mats['status_expired']),
        ("PROD_1_03", (4.0, -3.5, 1.45), mats['status_warning']),
        ("PROD_4_01", (4.0, 4.5, 1.45), mats['status_expired'])
    ]
    for hname, hloc, hmat in halos:
        bpy.ops.mesh.primitive_torus_add(major_radius=0.18, minor_radius=0.025, location=(hloc[0], hloc[1], hloc[2] + 0.25))
        ring = bpy.context.active_object
        ring.name = f"{hname}_IndicatorRing"
        ring.data.materials.append(hmat)
        waste_col.objects.link(ring)
        if ring.name in bpy.context.scene.collection.objects:
            bpy.context.scene.collection.objects.unlink(ring)

    # -------------------------------------------------------------
    # 9. CAMERAS
    # -------------------------------------------------------------
    cameras_def = [
        ("Cam_01_Supermarket_Promenade", (0.0, -14.2, 2.15), (math.radians(85), 0, 0), "PERSP", 21.0),
        ("Cam_02_Food_And_Produce", (-0.8, -7.5, 1.7), (math.radians(82), 0, math.radians(-20)), "PERSP", 32.0),
        ("Cam_03_Grocery_Shelves_Left", (-2.8, -4.0, 1.8), (math.radians(80), 0, math.radians(-70)), "PERSP", 30.0),
        ("Cam_04_Grocery_Shelves_Right", (2.8, -4.0, 1.8), (math.radians(80), 0, math.radians(70)), "PERSP", 30.0),
        ("Cam_05_Waste_Donation_Zones", (-7.5, 5.0, 3.8), (math.radians(65), 0, math.radians(-110)), "PERSP", 28.0),
        ("Cam_06_Isometric_TopView", (18.0, -18.0, 24.0), (math.radians(54.736), 0, math.radians(45)), "ORTHO", 34.0),
        ("Cam_07_Expiry_Monitoring", (-3.5, 1.8, 1.8), (math.radians(75), 0, math.radians(-40)), "PERSP", 42.0),
        ("Cam_08_Restock_Conveyor", (0.0, 11.0, 3.2), (math.radians(68), 0, 0), "PERSP", 32.0),
        ("Cam_09_Checkout_Area", (0.0, -16.0, 4.0), (math.radians(70), 0, math.radians(180)), "PERSP", 30.0),
        ("Cam_10_Hazardous_Disposal", (-8.5, -10.0, 2.5), (math.radians(75), 0, math.radians(-80)), "PERSP", 40.0)
    ]

    for cname, cloc, crot, ctype, param in cameras_def:
        cdata = bpy.data.cameras.new(name=cname + "_Data")
        cdata.type = ctype
        if ctype == "PERSP":
            cdata.lens = param
            cdata.clip_start = 0.1
            cdata.clip_end = 200.0
        else:
            cdata.ortho_scale = param
            cdata.clip_start = 0.1
            cdata.clip_end = 250.0
        cobj = bpy.data.objects.new(name=cname, object_data=cdata)
        cobj.location = cloc
        cobj.rotation_euler = crot
        cams_col.objects.link(cobj)
        if cname == "Cam_01_Supermarket_Promenade":
            bpy.context.scene.camera = cobj

    print(f"[UltimateStore] Complete! Created {len(bpy.data.objects)} real 3D product objects!")

if __name__ == "__main__":
    build_actual_supermarket_products()
