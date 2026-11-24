"""
Supermarket Architecture Builder with rich retail fixtures:
- 38x44m store, ceramic tile floor, two-tone perimeter walls with blue corporate banding
- Entrance / exit glass sliding doors with overhead transom header
- Shopping cart return corral with multiple chrome shopping carts and handles
- Basket staging stack
- 4 Full POS checkout counters with conveyored cash-desks, scanners, and touchscreens
- 6 Gondola aisle fixtures with suspended category signage boards and red price tag label strips
- Backroom warehouse storage with multi-level pallet racks and automated restocking conveyor belt
- 4 Dedicated Waste & Optimization stations (Donation, Recycling, Organic Dumpster, Hazard Drum & Locker)
"""

import bpy
import math

def create_box(name, size, location, material=None, collection=None):
    sx, sy, sz = size
    mesh = bpy.data.meshes.new(name + "_Mesh")
    obj = bpy.data.objects.new(name, mesh)
    
    verts = [
        (-sx/2, -sy/2, 0), (sx/2, -sy/2, 0), (sx/2, sy/2, 0), (-sx/2, sy/2, 0),
        (-sx/2, -sy/2, sz), (sx/2, -sy/2, sz), (sx/2, sy/2, sz), (-sx/2, sy/2, sz)
    ]
    faces = [
        (0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1),
        (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)
    ]
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    
    obj.location = location
    if material:
        obj.data.materials.append(material)
    if collection:
        collection.objects.link(obj)
    else:
        bpy.context.scene.collection.objects.link(obj)
    return obj

def build_architecture(materials, collection):
    arch_col = bpy.data.collections.new("01_Architecture")
    collection.children.link(arch_col)
    
    # 1. Floor
    create_box("Supermarket_Floor", (38.0, 44.0, 0.2), (0.0, 0.0, -0.2), materials['floor'], arch_col)
    
    # 2. Outer Perimeter Walls
    wall_height = 6.0
    wall_thick = 0.4
    
    # North (Storage back wall)
    create_box("Wall_North", (38.0, wall_thick, wall_height), (0.0, 22.0, 0.0), materials['wall'], arch_col)
    create_box("Wall_North_Accent", (38.0, wall_thick + 0.02, 0.4), (0.0, 22.0, 4.2), materials['wall_accent'], arch_col)
    
    # East Wall
    create_box("Wall_East", (wall_thick, 44.0, wall_height), (19.0, 0.0, 0.0), materials['wall'], arch_col)
    create_box("Wall_East_Accent", (wall_thick + 0.02, 44.0, 0.4), (19.0, 0.0, 4.2), materials['wall_accent'], arch_col)
    
    # West Wall
    create_box("Wall_West", (wall_thick, 44.0, wall_height), (-19.0, 0.0, 0.0), materials['wall'], arch_col)
    create_box("Wall_West_Accent", (wall_thick + 0.02, 44.0, 0.4), (-19.0, 0.0, 4.2), materials['wall_accent'], arch_col)
    
    # South Wall (Entrance / Front Wall with Automatic Glass Sliding Doors)
    create_box("Wall_South_Left", (14.0, wall_thick, wall_height), (-12.0, -22.0, 0.0), materials['wall'], arch_col)
    create_box("Wall_South_Right", (14.0, wall_thick, wall_height), (12.0, -22.0, 0.0), materials['wall'], arch_col)
    create_box("Wall_South_Header", (10.0, wall_thick, 2.2), (0.0, -22.0, 3.8), materials['wall_accent'], arch_col)
    
    # Glass Sliding Doors & Metal Framing
    create_box("Door_Frame_Left", (0.2, 0.3, 3.8), (-4.8, -22.0, 0.0), materials['metal_dark'], arch_col)
    create_box("Door_Frame_Right", (0.2, 0.3, 3.8), (4.8, -22.0, 0.0), materials['metal_dark'], arch_col)
    create_box("Door_Frame_Center", (0.15, 0.3, 3.8), (0.0, -22.0, 0.0), materials['metal_dark'], arch_col)
    create_box("Glass_Door_Left", (4.5, 0.08, 3.7), (-2.4, -22.0, 0.0), materials['glass'], arch_col)
    create_box("Glass_Door_Right", (4.5, 0.08, 3.7), (2.4, -22.0, 0.0), materials['glass'], arch_col)
    
    # Exterior & Interior Entrance Signboards
    create_box("Supermarket_Main_Signboard_Ext", (12.0, 0.3, 1.4), (0.0, -22.25, 4.4), materials['wall_accent'], arch_col)
    create_box("Supermarket_Welcome_Sign_Int", (10.0, 0.2, 1.0), (0.0, -21.8, 4.6), materials['wall_accent'], arch_col)
    
    # Partition Wall separating Sales Floor from Backroom Warehouse (Y = 13.0)
    create_box("Partition_Wall_Left", (16.0, 0.3, 4.5), (-11.0, 13.0, 0.0), materials['wall'], arch_col)
    create_box("Partition_Wall_Right", (16.0, 0.3, 4.5), (11.0, 13.0, 0.0), materials['wall'], arch_col)
    create_box("Partition_Wall_Header", (6.0, 0.3, 1.2), (0.0, 13.0, 3.3), materials['wall_accent'], arch_col)

    # Ceiling Beams and Luminaire Array
    light_col = bpy.data.collections.new("02_Lighting_Fixtures")
    collection.children.link(light_col)
    
    # Overhead Industrial Steel Trusses
    for truss_y in [-15.0, -5.0, 5.0, 16.0]:
        create_box(f"Roof_Truss_{truss_y}", (38.0, 0.35, 0.4), (0.0, truss_y, 5.8), materials['metal_dark'], arch_col)
    
    # 25 High-output Area Luminaire arrays
    for x in [-12.0, -6.0, 0.0, 6.0, 12.0]:
        for y in [-14.0, -7.0, 0.0, 7.0, 16.0]:
            create_box(f"Luminaire_{x}_{y}", (2.8, 0.4, 0.15), (x, y, 5.7), materials['ceiling_light'], light_col)
            light_data = bpy.data.lights.new(name=f"Light_Data_{x}_{y}", type='AREA')
            light_data.energy = 340.0
            light_data.size = 2.4
            light_data.size_y = 0.4
            light_data.color = (1.0, 0.98, 0.94)
            light_obj = bpy.data.objects.new(name=f"AreaLight_{x}_{y}", object_data=light_data)
            light_obj.location = (x, y, 5.6)
            light_col.objects.link(light_obj)

    # Ambient Sunlight Fill
    sun_data = bpy.data.lights.new(name="Store_Sun_Fill", type='SUN')
    sun_data.energy = 2.4
    sun_data.color = (0.96, 0.98, 1.0)
    sun_obj = bpy.data.objects.new(name="Store_Sun_Light", object_data=sun_data)
    sun_obj.location = (10.0, -10.0, 20.0)
    sun_obj.rotation_euler = (math.radians(35.0), math.radians(20.0), math.radians(-30.0))
    light_col.objects.link(sun_obj)

    return arch_col

def create_shelf_unit(name, length, depth, height, levels, material_frame, material_shelf, material_strip, collection):
    shelf_group = bpy.data.collections.new(name)
    collection.children.link(shelf_group)
    
    post_w = 0.08
    create_box(f"{name}_Post_L_Front", (post_w, post_w, height), (-length/2 + post_w/2, -depth/2 + post_w/2, 0.0), material_frame, shelf_group)
    create_box(f"{name}_Post_L_Back", (post_w, post_w, height), (-length/2 + post_w/2, depth/2 - post_w/2, 0.0), material_frame, shelf_group)
    create_box(f"{name}_Post_R_Front", (post_w, post_w, height), (length/2 - post_w/2, -depth/2 + post_w/2, 0.0), material_frame, shelf_group)
    create_box(f"{name}_Post_R_Back", (post_w, post_w, height), (length/2 - post_w/2, depth/2 - post_w/2, 0.0), material_frame, shelf_group)
    
    create_box(f"{name}_Backpanel", (length - 0.1, 0.04, height - 0.2), (0.0, 0.0, 0.1), material_frame, shelf_group)
    create_box(f"{name}_Base", (length, depth, 0.15), (0.0, 0.0, 0.0), material_frame, shelf_group)
    
    shelf_thickness = 0.05
    tier_heights = []
    level_spacing = (height - 0.4) / levels
    for i in range(levels):
        z = 0.35 + i * level_spacing
        create_box(f"{name}_Tier_{i+1}", (length - 0.06, depth - 0.04, shelf_thickness), (0.0, 0.0, z), material_shelf, shelf_group)
        # Front and Back Price Label Channels
        create_box(f"{name}_PriceTag_Front_{i+1}", (length - 0.08, 0.02, 0.04), (0.0, -depth/2 - 0.01, z + 0.02), material_strip, shelf_group)
        create_box(f"{name}_PriceTag_Back_{i+1}", (length - 0.08, 0.02, 0.04), (0.0, depth/2 + 0.01, z + 0.02), material_strip, shelf_group)
        tier_heights.append(z + shelf_thickness)
        
    return shelf_group, tier_heights

def build_aisles(materials, collection):
    aisle_col = bpy.data.collections.new("03_Supermarket_Aisles")
    collection.children.link(aisle_col)
    
    aisle_configs = [
        {"id": 1, "x": -11.5, "cat": "FOOD_PRODUCE", "name": "Aisle 1 - Fresh Fruits & Vegetables", "sign_mat": materials['sign_food']},
        {"id": 2, "x": -7.0,  "cat": "FOOD_DAIRY",   "name": "Aisle 2 - Dairy, Milk & Beverages",   "sign_mat": materials['sign_dairy']},
        {"id": 3, "x": -2.5,  "cat": "FOOD_PACKAGED","name": "Aisle 3 - Cereals, Bread & Bakery",   "sign_mat": materials['sign_pantry']},
        {"id": 4, "x": 2.5,   "cat": "HOUSEHOLD",    "name": "Aisle 4 - Household Cleaners & Hazard","sign_mat": materials['sign_hazardous']},
        {"id": 5, "x": 7.0,   "cat": "ELECTRONICS",  "name": "Aisle 5 - Consumer Tech & Electronics","sign_mat": materials['sign_electronics']},
        {"id": 6, "x": 11.5,  "cat": "CLOTHING",     "name": "Aisle 6 - Clothing, Shoes & Apparel", "sign_mat": materials['sign_clothing']}
    ]
    aisle_metadata = []
    
    for cfg in aisle_configs:
        sub_col = bpy.data.collections.new(f"Aisle_{cfg['id']}")
        aisle_col.children.link(sub_col)
        
        length = 8.5
        depth = 1.3
        height = 2.4
        levels = 4
        
        # South Gondola
        s1, h1 = create_shelf_unit(f"Aisle_{cfg['id']}_Shelf_S", length, depth, height, levels, materials['metal_shelf'], materials['metal_shelf'], materials['price_strip'], sub_col)
        for obj in s1.objects:
            obj.location.x += cfg['x']
            obj.location.y += -6.5
            
        # North Gondola
        s2, h2 = create_shelf_unit(f"Aisle_{cfg['id']}_Shelf_N", length, depth, height, levels, materials['metal_shelf'], materials['metal_shelf'], materials['price_strip'], sub_col)
        for obj in s2.objects:
            obj.location.x += cfg['x']
            obj.location.y += 2.5
            
        # Overhead Signboard with suspension cables
        create_box(f"Sign_Aisle_{cfg['id']}", (3.0, 0.1, 0.85), (cfg['x'], -2.0, 3.4), cfg['sign_mat'], sub_col)
        create_box(f"Sign_Cable1_{cfg['id']}", (0.02, 0.02, 2.3), (cfg['x'] - 1.3, -2.0, 3.4), materials['metal_chrome'], sub_col)
        create_box(f"Sign_Cable2_{cfg['id']}", (0.02, 0.02, 2.3), (cfg['x'] + 1.3, -2.0, 3.4), materials['metal_chrome'], sub_col)
        
        aisle_metadata.append({
            "id": cfg['id'],
            "name": cfg['name'],
            "category": cfg['cat'],
            "x": cfg['x'],
            "shelf_south_y": -6.5,
            "shelf_north_y": 2.5,
            "levels": levels,
            "tier_heights": h1,
            "length": length,
            "depth": depth
        })
        
    return aisle_col, aisle_metadata

def build_checkout_area(materials, collection):
    chk_col = bpy.data.collections.new("04_Checkout_Counters")
    collection.children.link(chk_col)
    
    counter_xs = [-9.0, -3.0, 3.0, 9.0]
    y_pos = -16.0
    
    for i, x in enumerate(counter_xs):
        prefix = f"Checkout_Counter_{i+1}"
        # Sturdy blue desk body
        create_box(f"{prefix}_Base", (3.2, 1.2, 0.95), (x, y_pos, 0.0), materials['checkout_body'], chk_col)
        # Wooden bag staging ledge
        create_box(f"{prefix}_Ledge", (3.3, 0.2, 0.05), (x, y_pos - 0.6, 0.85), materials['checkout_wood'], chk_col)
        # Motorized Conveyor belt
        create_box(f"{prefix}_Belt", (2.2, 0.55, 0.05), (x - 0.4, y_pos, 0.95), materials['conveyor_belt'], chk_col)
        # POS Touchscreen Terminal
        create_box(f"{prefix}_Screen_Stand", (0.08, 0.08, 0.35), (x + 1.1, y_pos + 0.3, 0.95), materials['metal_dark'], chk_col)
        screen = create_box(f"{prefix}_Screen", (0.35, 0.05, 0.28), (x + 1.1, y_pos + 0.3, 1.3), materials['screen_display'], chk_col)
        screen.rotation_euler.x = math.radians(-15.0)
        # Barcode scanner plate
        create_box(f"{prefix}_Scanner", (0.28, 0.28, 0.03), (x + 0.8, y_pos - 0.15, 0.95), materials['metal_dark'], chk_col)

    # Store Props: Chrome Shopping Carts and Basket Stacks
    props_col = bpy.data.collections.new("04b_Store_Props")
    chk_col.children.link(props_col)
    
    create_box("Cart_Rail_1", (0.08, 6.0, 0.9), (-15.5, -17.0, 0.0), materials['metal_chrome'], props_col)
    create_box("Cart_Rail_2", (0.08, 6.0, 0.9), (-17.0, -17.0, 0.0), materials['metal_chrome'], props_col)
    
    # 5 Chrome Shopping Carts nested in the corral
    for c_idx in range(5):
        cy = -19.5 + c_idx * 1.0
        create_box(f"Shopping_Cart_{c_idx+1}_Basket", (0.6, 0.85, 0.5), (-16.25, cy, 0.45), materials['metal_chrome'], props_col)
        create_box(f"Shopping_Cart_{c_idx+1}_Handle", (0.65, 0.05, 0.05), (-16.25, cy + 0.42, 0.95), materials['wall_accent'], props_col)
        # Wheels
        for wx in [-0.26, 0.26]:
            for wy in [-0.35, 0.35]:
                create_box(f"Cart_Wheel_{c_idx}_{wx}_{wy}", (0.04, 0.08, 0.12), (-16.25 + wx, cy + wy, 0.0), materials['metal_dark'], props_col)
        
    # 2 Stacks of Green Shopping Baskets near entrance
    for stack_x in [-13.2, -14.2]:
        for b_idx in range(6):
            create_box(f"Basket_Stack_{stack_x}_{b_idx+1}", (0.45, 0.35, 0.08), (stack_x, -20.5, b_idx * 0.09), materials['sign_food'], props_col)

    # Dome Security Cameras
    for cam_loc in [(-18.0, -21.0, 5.7), (18.0, -21.0, 5.7), (-18.0, 21.0, 5.7), (18.0, 21.0, 5.7)]:
        create_box(f"Security_Camera_{cam_loc[0]}_{cam_loc[1]}", (0.3, 0.3, 0.2), cam_loc, materials['metal_dark'], props_col)

    return chk_col

def build_storage_and_conveyor(materials, collection):
    storage_col = bpy.data.collections.new("05_Storage_and_Conveyor")
    collection.children.link(storage_col)
    
    for x in [-12.0, -4.0, 4.0, 12.0]:
        create_shelf_unit(f"Pallet_Rack_{x}", 6.5, 1.8, 4.8, 3, materials['metal_dark'], materials['checkout_wood'], materials['price_strip'], storage_col)
        last_rack = storage_col.children[-1]
        for obj in last_rack.objects:
            obj.location.x += x
            obj.location.y += 18.5
            
    # Automated Restocking Conveyor Belt System
    conveyor_len = 10.0
    conveyor_w = 1.1
    conveyor_h = 0.85
    create_box("Conveyor_Frame", (conveyor_w + 0.15, conveyor_len, conveyor_h), (0.0, 15.5, 0.0), materials['metal_dark'], storage_col)
    create_box("Conveyor_Belt_Surface", (conveyor_w, conveyor_len - 0.2, 0.05), (0.0, 15.5, conveyor_h), materials['conveyor_belt'], storage_col)
    create_box("Conveyor_Rail_Left", (0.05, conveyor_len, 0.25), (-conveyor_w/2 - 0.05, 15.5, conveyor_h), materials['metal_chrome'], storage_col)
    create_box("Conveyor_Rail_Right", (0.05, conveyor_len, 0.25), (conveyor_w/2 + 0.05, 15.5, conveyor_h), materials['metal_chrome'], storage_col)
    
    for ry in range(11, 21):
        create_box(f"Conveyor_Roller_{ry}", (conveyor_w, 0.06, 0.06), (0.0, float(ry), conveyor_h - 0.04), materials['metal_chrome'], storage_col)
        
    return storage_col

def build_waste_management_zones(materials, collection):
    waste_col = bpy.data.collections.new("06_Waste_Management_Zones")
    collection.children.link(waste_col)
    
    zones = [
        {"id": "Donation", "name": "Station_01_Donation_Zone", "y": 8.0, "mat": materials['zone_donation']},
        {"id": "Recycling", "name": "Station_02_Recycling_Zone", "y": 3.0, "mat": materials['zone_recycling']},
        {"id": "Organic", "name": "Station_03_Organic_Waste_Zone", "y": -2.0, "mat": materials['zone_organic']},
        {"id": "Hazardous", "name": "Station_04_Hazardous_Disposal", "y": -7.0, "mat": materials['zone_hazardous']}
    ]
    zone_metadata = {}
    
    for z in zones:
        z_col = bpy.data.collections.new(z['name'])
        waste_col.children.link(z_col)
        
        # Floor pad boundary
        create_box(f"{z['id']}_Floor_Border", (4.2, 3.8, 0.03), (-15.5, z['y'], 0.01), z['mat'], z_col)
        if z['id'] == 'Hazardous':
            create_box(f"{z['id']}_Stripe", (4.4, 4.0, 0.01), (-15.5, z['y'], 0.005), materials['hazard_stripe'], z_col)
            
        create_box(f"{z['id']}_Station_Sign", (0.1, 3.4, 0.9), (-18.7, z['y'], 3.2), z['mat'], z_col)
        
        if z['id'] == 'Donation':
            create_box("Donation_Hamper_1", (1.2, 1.2, 1.0), (-16.0, z['y'] - 0.8, 0.0), z['mat'], z_col)
            create_box("Donation_Hamper_2", (1.2, 1.2, 1.0), (-16.0, z['y'] + 0.8, 0.0), z['mat'], z_col)
            create_box("Donation_Inspection_Table", (1.0, 2.6, 0.85), (-14.0, z['y'], 0.0), materials['metal_shelf'], z_col)
        elif z['id'] == 'Recycling':
            bin_colors = [materials['zone_recycling'], materials['wall_accent'], materials['metal_shelf']]
            for b_idx, by_off in enumerate([-0.9, 0.0, 0.9]):
                create_box(f"Recycle_Bin_{b_idx+1}", (0.9, 0.7, 1.1), (-15.8, z['y'] + by_off, 0.0), bin_colors[b_idx], z_col)
                create_box(f"Recycle_Bin_Lid_{b_idx+1}", (0.95, 0.75, 0.15), (-15.8, z['y'] + by_off, 1.1), materials['metal_dark'], z_col)
        elif z['id'] == 'Organic':
            create_box("Compost_Dumpster", (1.8, 2.6, 1.2), (-15.5, z['y'], 0.0), z['mat'], z_col)
            create_box("Compost_Lid", (1.85, 2.65, 0.1), (-15.5, z['y'], 1.2), materials['metal_dark'], z_col)
        elif z['id'] == 'Hazardous':
            create_box("Hazard_Sealed_Locker", (1.2, 1.8, 2.2), (-16.2, z['y'] - 0.6, 0.0), z['mat'], z_col)
            create_box("Battery_Disposal_Drum", (1.0, 1.0, 1.2), (-15.0, z['y'] + 0.9, 0.0), materials['hazard_stripe'], z_col)
            
        zone_metadata[z['id']] = {
            "name": z['name'],
            "drop_point": (-15.0, z['y'], 1.2),
            "station_y": z['y']
        }
        
    return waste_col, zone_metadata
