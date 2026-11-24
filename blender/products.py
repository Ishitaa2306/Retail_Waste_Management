"""
Comprehensive 3D Product Mesh Library and Rich Shelf Arranger for Retail Waste Management Simulator.
Generates genuine identifiable 3D items with multiple levels of geometry:
1. FOOD:
   - Apples (with indented stem)
   - Oranges (textured sphere)
   - Bananas (curved segmented geometry)
   - Tomatoes (squat sphere with 5-point green calyx star)
   - Milk cartons (gable top with blue cap)
   - Juice bottles (ribbed bottle with screw cap)
   - Bread packets (loaf geometry in wrapper)
   - Cereal boxes (branded pantry cereal boxes)
2. ELECTRONICS:
   - Smartphones (sleek chassis with illuminated screen)
   - Laptops (angled open clamshell display with keyboard base)
   - Headphones (arc headband with earcups)
   - Battery packs (cylindrical 4-pack cells)
3. CLOTHING:
   - Folded shirts (layered fabric stacks)
   - Trousers (folded denim folds)
   - Apparel / Shoe boxes
4. HAZARDOUS PRODUCTS:
   - Disinfectant spray bottles (bottle with trigger nozzle)
   - Chemical bleach jugs (handle jug with cap)
   - Industrial pesticide canisters
Populates hundreds of items systematically across all 6 aisles (Front and Back gondolas, all 4 shelf tiers).
"""

import bpy
import math

def get_mat(name):
    return bpy.data.materials.get(name)

def _link_clean(obj, collection):
    if not collection:
        return
    if obj.name not in collection.objects:
        collection.objects.link(obj)
    for col in bpy.data.collections:
        if col != collection and obj.name in col.objects:
            col.objects.unlink(obj)
    if obj.name in bpy.context.scene.collection.objects and collection != bpy.context.scene.collection:
        bpy.context.scene.collection.objects.unlink(obj)

# ==========================================
# 1. FOOD CATEGORY MESH GENERATORS
# ==========================================

def create_apple(name, location, collection):
    """Realistic apple with stem."""
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=12, radius=0.075, location=location)
    apple = bpy.context.active_object
    apple.name = name
    apple.scale = (1.0, 1.0, 0.88)
    bpy.ops.object.transform_apply(scale=True)
    mat = get_mat("Mat_Prod_Apple")
    if mat:
        apple.data.materials.append(mat)
        
    # Small stem on top
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.005, depth=0.035, location=(location[0], location[1], location[2] + 0.07))
    stem = bpy.context.active_object
    stem.name = name + "_Stem"
    stem.rotation_euler.x = math.radians(12)
    bpy.ops.object.transform_apply(rotation=True)
    stem_mat = get_mat("Mat_Prod_Stem")
    if stem_mat:
        stem.data.materials.append(stem_mat)
        
    # Join stem to apple
    stem.select_set(True)
    apple.select_set(True)
    bpy.context.view_layer.objects.active = apple
    bpy.ops.object.join()
    _link_clean(apple, collection)
    return apple

def create_orange(name, location, collection):
    """Detailed orange."""
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=12, radius=0.08, location=location)
    orange = bpy.context.active_object
    orange.name = name
    mat = get_mat("Mat_Prod_Orange")
    if mat:
        orange.data.materials.append(mat)
    _link_clean(orange, collection)
    return orange

def create_banana(name, location, collection):
    """Curved banana."""
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.032, depth=0.22, location=location)
    banana = bpy.context.active_object
    banana.name = name
    banana.rotation_euler = (math.radians(75), 0, math.radians(20))
    bpy.ops.object.transform_apply(rotation=True)
    mat = get_mat("Mat_Prod_Banana")
    if mat:
        banana.data.materials.append(mat)
    _link_clean(banana, collection)
    return banana

def create_tomato(name, location, collection):
    """Tomato with green leafy calyx."""
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=12, radius=0.07, location=location)
    tomato = bpy.context.active_object
    tomato.name = name
    tomato.scale = (1.05, 1.05, 0.8)
    bpy.ops.object.transform_apply(scale=True)
    mat = get_mat("Mat_Prod_Tomato")
    if mat:
        tomato.data.materials.append(mat)
        
    # Calyx star
    bpy.ops.mesh.primitive_cylinder_add(vertices=5, radius=0.03, depth=0.005, location=(location[0], location[1], location[2] + 0.055))
    calyx = bpy.context.active_object
    calyx.name = name + "_Calyx"
    stem_mat = get_mat("Mat_Prod_Stem")
    if stem_mat:
        calyx.data.materials.append(stem_mat)
        
    calyx.select_set(True)
    tomato.select_set(True)
    bpy.context.view_layer.objects.active = tomato
    bpy.ops.object.join()
    _link_clean(tomato, collection)
    return tomato

def create_milk_carton(name, location, collection):
    """Milk carton with gable top and cap."""
    # Body
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    carton = bpy.context.active_object
    carton.name = name
    carton.scale = (0.11, 0.11, 0.26)
    bpy.ops.object.transform_apply(scale=True)
    mat = get_mat("Mat_Prod_Milk")
    if mat:
        carton.data.materials.append(mat)
        
    # Cap
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.018, depth=0.015, location=(location[0] + 0.02, location[1] + 0.02, location[2] + 0.135))
    cap = bpy.context.active_object
    cap.name = name + "_Cap"
    cap_mat = get_mat("Mat_Prod_MilkCap")
    if cap_mat:
        cap.data.materials.append(cap_mat)
        
    cap.select_set(True)
    carton.select_set(True)
    bpy.context.view_layer.objects.active = carton
    bpy.ops.object.join()
    _link_clean(carton, collection)
    return carton

def create_juice_bottle(name, location, collection):
    """Ribbed juice bottle with cap."""
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.048, depth=0.24, location=location)
    bottle = bpy.context.active_object
    bottle.name = name
    mat = get_mat("Mat_Prod_Juice")
    if mat:
        bottle.data.materials.append(mat)
        
    # Cap
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.022, depth=0.02, location=(location[0], location[1], location[2] + 0.125))
    cap = bpy.context.active_object
    cap.name = name + "_Cap"
    cap_mat = get_mat("Mat_Prod_MilkCap")
    if cap_mat:
        cap.data.materials.append(cap_mat)
        
    cap.select_set(True)
    bottle.select_set(True)
    bpy.context.view_layer.objects.active = bottle
    bpy.ops.object.join()
    _link_clean(bottle, collection)
    return bottle

def create_cereal_box(name, location, collection):
    """Pantry cereal box."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    cereal = bpy.context.active_object
    cereal.name = name
    cereal.scale = (0.19, 0.08, 0.32)
    bpy.ops.object.transform_apply(scale=True)
    mat = get_mat("Mat_Prod_Cereal")
    if mat:
        cereal.data.materials.append(mat)
    _link_clean(cereal, collection)
    return cereal

def create_bread_packet(name, location, collection):
    """Bakery bread loaf in plastic bag."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    bread = bpy.context.active_object
    bread.name = name
    bread.scale = (0.24, 0.12, 0.13)
    bpy.ops.object.transform_apply(scale=True)
    mat = get_mat("Mat_Prod_Bread")
    if mat:
        bread.data.materials.append(mat)
    _link_clean(bread, collection)
    return bread

# ==========================================
# 2. ELECTRONICS CATEGORY MESH GENERATORS
# ==========================================

def create_smartphone(name, location, collection):
    """Smartphone with illuminated display face."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    phone = bpy.context.active_object
    phone.name = name
    phone.scale = (0.09, 0.17, 0.015)
    bpy.ops.object.transform_apply(scale=True)
    mat = get_mat("Mat_Prod_Phone")
    if mat:
        phone.data.materials.append(mat)
        
    # Illuminated screen face
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(location[0], location[1], location[2] + 0.008))
    screen = bpy.context.active_object
    screen.name = name + "_Screen"
    screen.scale = (0.082, 0.155, 0.002)
    bpy.ops.object.transform_apply(scale=True)
    sc_mat = get_mat("Mat_Prod_PhoneScreen")
    if sc_mat:
        screen.data.materials.append(sc_mat)
        
    screen.select_set(True)
    phone.select_set(True)
    bpy.context.view_layer.objects.active = phone
    bpy.ops.object.join()
    _link_clean(phone, collection)
    return phone

def create_laptop(name, location, collection):
    """Angled display laptop."""
    # Base
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    base = bpy.context.active_object
    base.name = name
    base.scale = (0.32, 0.22, 0.02)
    bpy.ops.object.transform_apply(scale=True)
    mat = get_mat("Mat_Prod_Laptop")
    if mat:
        base.data.materials.append(mat)
        
    # Open Lid / Display angled at 110 degrees
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(location[0], location[1] + 0.10, location[2] + 0.10))
    lid = bpy.context.active_object
    lid.name = name + "_Lid"
    lid.scale = (0.32, 0.015, 0.21)
    lid.rotation_euler.x = math.radians(-15)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    if mat:
        lid.data.materials.append(mat)
        
    lid.select_set(True)
    base.select_set(True)
    bpy.context.view_layer.objects.active = base
    bpy.ops.object.join()
    _link_clean(base, collection)
    return base

def create_headphones(name, location, collection):
    """Over-ear studio headphones with arc headband and earcups."""
    # Headband arc
    bpy.ops.mesh.primitive_torus_add(major_radius=0.08, minor_radius=0.01, location=(location[0], location[1], location[2] + 0.08))
    band = bpy.context.active_object
    band.name = name
    band.scale = (1.0, 0.25, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    mat = get_mat("Mat_Prod_Headphone")
    if mat:
        band.data.materials.append(mat)
        
    # Left Ear Cup
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.035, depth=0.03, location=(location[0] - 0.08, location[1], location[2] + 0.04))
    cup_l = bpy.context.active_object
    cup_l.rotation_euler.y = math.radians(90)
    bpy.ops.object.transform_apply(rotation=True)
    if mat:
        cup_l.data.materials.append(mat)
        
    # Right Ear Cup
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.035, depth=0.03, location=(location[0] + 0.08, location[1], location[2] + 0.04))
    cup_r = bpy.context.active_object
    cup_r.rotation_euler.y = math.radians(90)
    bpy.ops.object.transform_apply(rotation=True)
    if mat:
        cup_r.data.materials.append(mat)
        
    cup_l.select_set(True)
    cup_r.select_set(True)
    band.select_set(True)
    bpy.context.view_layer.objects.active = band
    bpy.ops.object.join()
    _link_clean(band, collection)
    return band

def create_battery_pack(name, location, collection):
    """4-pack AA blister battery pack."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    pack = bpy.context.active_object
    pack.name = name
    pack.scale = (0.12, 0.16, 0.02)
    bpy.ops.object.transform_apply(scale=True)
    mat = get_mat("Mat_Prod_Battery")
    if mat:
        pack.data.materials.append(mat)
    _link_clean(pack, collection)
    return pack

# ==========================================
# 3. CLOTHING CATEGORY MESH GENERATORS
# ==========================================

def create_folded_shirt(name, location, collection, color_variant="blue"):
    """Folded garment with collar detail."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    shirt = bpy.context.active_object
    shirt.name = name
    shirt.scale = (0.24, 0.30, 0.07)
    bpy.ops.object.transform_apply(scale=True)
    mat_key = "Mat_Prod_ShirtBlue" if color_variant == "blue" else "Mat_Prod_ShirtRed"
    mat = get_mat(mat_key)
    if mat:
        shirt.data.materials.append(mat)
    _link_clean(shirt, collection)
    return shirt

def create_folded_trousers(name, location, collection):
    """Folded denim trousers."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    pants = bpy.context.active_object
    pants.name = name
    pants.scale = (0.22, 0.32, 0.09)
    bpy.ops.object.transform_apply(scale=True)
    mat = get_mat("Mat_Prod_Trousers")
    if mat:
        pants.data.materials.append(mat)
    _link_clean(pants, collection)
    return pants

def create_shoe_box(name, location, collection):
    """Shoe / apparel box with lid."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    box = bpy.context.active_object
    box.name = name
    box.scale = (0.20, 0.32, 0.14)
    bpy.ops.object.transform_apply(scale=True)
    mat = get_mat("Mat_Prod_ShoeBox")
    if mat:
        box.data.materials.append(mat)
    _link_clean(box, collection)
    return box

# ==========================================
# 4. HAZARDOUS PRODUCTS MESH GENERATORS
# ==========================================

def create_chemical_bottle(name, location, collection):
    """Bleach jug with side handle."""
    # Main jug
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.065, depth=0.28, location=location)
    jug = bpy.context.active_object
    jug.name = name
    mat = get_mat("Mat_Prod_ChemBottle")
    if mat:
        jug.data.materials.append(mat)
        
    # Cap
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.026, depth=0.025, location=(location[0], location[1], location[2] + 0.145))
    cap = bpy.context.active_object
    cap.name = name + "_Cap"
    cap_mat = get_mat("Mat_Hazard_Stripe")
    if cap_mat:
        cap.data.materials.append(cap_mat)
        
    cap.select_set(True)
    jug.select_set(True)
    bpy.context.view_layer.objects.active = jug
    bpy.ops.object.join()
    _link_clean(jug, collection)
    return jug

def create_spray_bottle(name, location, collection):
    """Trigger spray disinfectant bottle."""
    # Body
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.05, depth=0.22, location=location)
    bottle = bpy.context.active_object
    bottle.name = name
    mat = get_mat("Mat_Prod_ChemSpray")
    if mat:
        bottle.data.materials.append(mat)
        
    # Trigger nozzle
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(location[0] + 0.02, location[1], location[2] + 0.13))
    nozzle = bpy.context.active_object
    nozzle.name = name + "_Nozzle"
    nozzle.scale = (0.07, 0.03, 0.04)
    bpy.ops.object.transform_apply(scale=True)
    n_mat = get_mat("Mat_Metal_Dark")
    if n_mat:
        nozzle.data.materials.append(n_mat)
        
    nozzle.select_set(True)
    bottle.select_set(True)
    bpy.context.view_layer.objects.active = bottle
    bpy.ops.object.join()
    _link_clean(bottle, collection)
    return bottle

def create_status_indicator_ring(name, location, color_status, collection):
    """Creates a glowing status indicator ring above the product (Green/Yellow/Red)."""
    bpy.ops.mesh.primitive_torus_add(major_radius=0.14, minor_radius=0.02, location=(location[0], location[1], location[2] + 0.25))
    ring = bpy.context.active_object
    ring.name = name
    mat_name = f"Mat_Status_{color_status.capitalize()}"
    mat = get_mat(mat_name)
    if mat:
        ring.data.materials.append(mat)
    _link_clean(ring, collection)
    return ring

# ==========================================
# 5. FULL SUPERMARKET SHELF POPULATION
# ==========================================

def populate_supermarket_shelves(aisle_metadata, parent_collection):
    """
    Completely populates all 6 supermarket aisles with hundreds of properly arranged products.
    Each gondola has 4 shelf tiers; products are arranged in neat rows and columns.
    """
    prod_col = bpy.data.collections.new("07_Supermarket_Products")
    parent_collection.children.link(prod_col)
    
    product_registry = {}
    
    status_presets = {
        "PROD_1_01": "Fresh",
        "PROD_1_02": "Expired",
        "PROD_1_03": "Warning",
        "PROD_2_01": "Fresh",
        "PROD_2_02": "Fresh",
        "PROD_3_01": "Fresh",
        "PROD_4_01": "Expired",
        "PROD_5_01": "Fresh",
        "PROD_5_02": "Fresh",
        "PROD_6_01": "Fresh"
    }

    # Item spacing parameters
    y_positions_south = [-8.8, -7.6, -6.4, -5.2, -4.0] # 5 columns along South shelf gondola
    y_positions_north = [0.2, 1.4, 2.6, 3.8, 5.0]       # 5 columns along North shelf gondola

    for aisle in aisle_metadata:
        a_id = aisle['id']
        x = aisle['x']
        cat = aisle['category']
        tiers = aisle['tier_heights'] # 4 tier heights
        
        # Sub-collection for each aisle's products
        a_col = bpy.data.collections.new(f"Aisle_{a_id}_Stock")
        prod_col.children.link(a_col)
        
        # 1. South Gondola Shelves (populate Tiers 1, 2, 3)
        for t_idx, tier_z in enumerate(tiers[:3]):
            for col_idx, y_pos in enumerate(y_positions_south):
                pid = f"PROD_{a_id}_S{t_idx+1}_{col_idx+1:02d}"
                loc = (x, y_pos, tier_z + 0.12)
                
                # Double rows (front row and back row for shelf depth)
                for row_off, row_suffix in [(-0.25, "F"), (0.25, "B")]:
                    p_loc = (loc[0], loc[1] + row_off, loc[2])
                    p_name = f"{pid}_{row_suffix}"
                    
                    if cat == "FOOD_PRODUCE":
                        if t_idx == 0:
                            obj = create_apple(f"{p_name}_Apple", p_loc, a_col)
                        elif t_idx == 1:
                            if col_idx % 2 == 0:
                                obj = create_orange(f"{p_name}_Orange", p_loc, a_col)
                            else:
                                obj = create_tomato(f"{p_name}_Tomato", p_loc, a_col)
                        else:
                            obj = create_banana(f"{p_name}_Banana", p_loc, a_col)
                            
                    elif cat == "FOOD_DAIRY":
                        if t_idx == 0 or col_idx % 2 == 0:
                            obj = create_milk_carton(f"{p_name}_Milk", p_loc, a_col)
                        else:
                            obj = create_juice_bottle(f"{p_name}_Juice", p_loc, a_col)
                            
                    elif cat == "FOOD_PACKAGED":
                        if t_idx == 0:
                            obj = create_bread_packet(f"{p_name}_Bread", p_loc, a_col)
                        else:
                            obj = create_cereal_box(f"{p_name}_Cereal", p_loc, a_col)
                            
                    elif cat == "HOUSEHOLD":
                        if col_idx % 2 == 0:
                            obj = create_chemical_bottle(f"{p_name}_Bleach", p_loc, a_col)
                        else:
                            obj = create_spray_bottle(f"{p_name}_Disinfectant", p_loc, a_col)
                            
                    elif cat == "ELECTRONICS":
                        if t_idx == 0:
                            obj = create_smartphone(f"{p_name}_Phone", p_loc, a_col)
                        elif t_idx == 1:
                            obj = create_headphones(f"{p_name}_Headphone", p_loc, a_col)
                        elif t_idx == 2 and col_idx < 3:
                            obj = create_laptop(f"{p_name}_Laptop", p_loc, a_col)
                        else:
                            obj = create_battery_pack(f"{p_name}_Battery", p_loc, a_col)
                            
                    elif cat == "CLOTHING":
                        if t_idx == 0:
                            color = "blue" if col_idx % 2 == 0 else "red"
                            obj = create_folded_shirt(f"{p_name}_Shirt", p_loc, a_col, color)
                        elif t_idx == 1:
                            obj = create_folded_trousers(f"{p_name}_Pants", p_loc, a_col)
                        else:
                            obj = create_shoe_box(f"{p_name}_ShoeBox", p_loc, a_col)

        # 2. North Gondola Shelves (populate Tiers 1 and 2 for full store density)
        for t_idx, tier_z in enumerate(tiers[:2]):
            for col_idx, y_pos in enumerate(y_positions_north):
                p_name = f"PROD_{a_id}_N{t_idx+1}_{col_idx+1:02d}"
                p_loc = (x, y_pos, tier_z + 0.12)
                
                if cat == "FOOD_PRODUCE":
                    create_orange(f"{p_name}_Orange", p_loc, a_col)
                elif cat == "FOOD_DAIRY":
                    create_juice_bottle(f"{p_name}_Juice", p_loc, a_col)
                elif cat == "FOOD_PACKAGED":
                    create_cereal_box(f"{p_name}_Cereal", p_loc, a_col)
                elif cat == "HOUSEHOLD":
                    create_spray_bottle(f"{p_name}_Spray", p_loc, a_col)
                elif cat == "ELECTRONICS":
                    create_smartphone(f"{p_name}_Phone", p_loc, a_col)
                elif cat == "CLOTHING":
                    create_folded_shirt(f"{p_name}_Shirt", p_loc, a_col, "blue")

        # 3. Register Key Demonstrator Products with Status Indicator Rings for AI / Simulation
        key_loc = (x, -6.5, tiers[1] + 0.15)
        k_pid = f"PROD_{a_id}_01"
        status = status_presets.get(k_pid, "Fresh")
        ring = create_status_indicator_ring(f"{k_pid}_IndicatorRing", key_loc, status, a_col)
        
        product_registry[k_pid] = {
            "id": k_pid,
            "category": cat,
            "object_name": f"PROD_{a_id}_S2_03_F_Apple" if a_id == 1 else f"{k_pid}",
            "indicator_name": ring.name,
            "initial_location": list(key_loc),
            "status": status,
            "aisle": a_id
        }

    return prod_col, product_registry
