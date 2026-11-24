"""
Materials module for Retail Waste Management Simulator.
Provides vibrant, realistic procedural PBR materials compatible with Blender 4.x & 5.x.
Includes category signage, metallic shelf brackets, packaging textures, food textures.
"""

import bpy

def get_or_create_material(name, base_color=(0.8, 0.8, 0.8, 1.0), roughness=0.5, metallic=0.0, emission_color=None, emission_strength=1.0, alpha=1.0):
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    node_output.location = (400, 0)
    node_principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_principled.location = (0, 0)
    
    if "Base Color" in node_principled.inputs:
        node_principled.inputs["Base Color"].default_value = base_color
    if "Roughness" in node_principled.inputs:
        node_principled.inputs["Roughness"].default_value = roughness
    if "Metallic" in node_principled.inputs:
        node_principled.inputs["Metallic"].default_value = metallic
        
    if emission_color:
        if "Emission Color" in node_principled.inputs:
            node_principled.inputs["Emission Color"].default_value = emission_color
        elif "Emission" in node_principled.inputs:
            node_principled.inputs["Emission"].default_value = emission_color
        if "Emission Strength" in node_principled.inputs:
            node_principled.inputs["Emission Strength"].default_value = emission_strength
            
    if alpha < 1.0:
        if "Alpha" in node_principled.inputs:
            node_principled.inputs["Alpha"].default_value = alpha
        mat.blend_method = 'BLEND'
        if hasattr(mat, 'shadow_method'):
            mat.shadow_method = 'HASHED'
            
    mat.node_tree.links.new(node_principled.outputs[0], node_output.inputs[0])
    return mat

def create_checker_floor_material(name="Supermarket_Floor_Tile"):
    if name in bpy.data.materials:
        return bpy.data.materials[name]
        
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    mapping = nodes.new(type='ShaderNodeMapping')
    mapping.inputs['Scale'].default_value = (38.0, 44.0, 1.0)
    
    checker = nodes.new(type='ShaderNodeTexChecker')
    checker.inputs['Color1'].default_value = (0.94, 0.95, 0.97, 1.0) # Bright clean white tile
    checker.inputs['Color2'].default_value = (0.82, 0.85, 0.89, 1.0) # Light modern grey tile
    checker.inputs['Scale'].default_value = 1.0
    
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.inputs['Roughness'].default_value = 0.12 # Clean polished gloss
    principled.inputs['Metallic'].default_value = 0.04
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    
    links = mat.node_tree.links
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], checker.inputs['Vector'])
    links.new(checker.outputs['Color'], principled.inputs['Base Color'])
    links.new(principled.outputs[0], output.inputs[0])
    return mat

def init_all_materials():
    materials = {}
    
    # Store Architecture
    materials['floor'] = create_checker_floor_material("Mat_Supermarket_Floor")
    materials['wall'] = get_or_create_material("Mat_Wall", (0.92, 0.94, 0.96, 1.0), roughness=0.6)
    materials['wall_accent'] = get_or_create_material("Mat_Wall_Accent", (0.05, 0.35, 0.75, 1.0), roughness=0.3)
    materials['wall_lower'] = get_or_create_material("Mat_Wall_Lower", (0.2, 0.25, 0.32, 1.0), roughness=0.4)
    materials['ceiling'] = get_or_create_material("Mat_Ceiling", (0.18, 0.20, 0.22, 1.0), roughness=0.85)
    materials['glass'] = get_or_create_material("Mat_Glass", (0.85, 0.95, 1.0, 1.0), roughness=0.03, alpha=0.25)
    materials['metal_dark'] = get_or_create_material("Mat_Metal_Dark", (0.12, 0.13, 0.15, 1.0), roughness=0.3, metallic=0.9)
    materials['metal_chrome'] = get_or_create_material("Mat_Metal_Chrome", (0.92, 0.93, 0.95, 1.0), roughness=0.08, metallic=0.98)
    materials['metal_shelf'] = get_or_create_material("Mat_Shelf_Rack", (0.90, 0.92, 0.94, 1.0), roughness=0.25, metallic=0.6)
    materials['shelf_wood'] = get_or_create_material("Mat_Shelf_Wood", (0.82, 0.62, 0.42, 1.0), roughness=0.45)
    
    # Lighting fixtures
    materials['ceiling_light'] = get_or_create_material("Mat_Ceiling_Light", (1.0, 1.0, 1.0, 1.0), emission_color=(1.0, 0.98, 0.92, 1.0), emission_strength=5.5)
    
    # Store Fixtures & Checkout
    materials['checkout_body'] = get_or_create_material("Mat_Checkout_Body", (0.18, 0.45, 0.72, 1.0), roughness=0.35)
    materials['checkout_wood'] = get_or_create_material("Mat_Checkout_Wood", (0.78, 0.54, 0.34, 1.0), roughness=0.4)
    materials['conveyor_belt'] = get_or_create_material("Mat_Conveyor_Rubber", (0.08, 0.08, 0.09, 1.0), roughness=0.65)
    materials['screen_display'] = get_or_create_material("Mat_POS_Screen", (0.05, 0.05, 0.08, 1.0), emission_color=(0.1, 0.75, 1.0, 1.0), emission_strength=3.0)
    materials['price_strip'] = get_or_create_material("Mat_Price_Strip", (0.98, 0.25, 0.15, 1.0), roughness=0.3)
    
    # 4 Waste Management & Optimization Station Materials
    materials['zone_donation'] = get_or_create_material("Mat_Zone_Donation", (0.12, 0.72, 0.28, 1.0), roughness=0.3)
    materials['zone_recycling'] = get_or_create_material("Mat_Zone_Recycling", (0.08, 0.48, 0.92, 1.0), roughness=0.3)
    materials['zone_organic'] = get_or_create_material("Mat_Zone_Organic", (0.78, 0.52, 0.12, 1.0), roughness=0.4)
    materials['zone_hazardous'] = get_or_create_material("Mat_Zone_Hazardous", (0.90, 0.12, 0.12, 1.0), roughness=0.3)
    materials['hazard_stripe'] = get_or_create_material("Mat_Hazard_Stripe", (0.98, 0.82, 0.02, 1.0), roughness=0.25)
    
    # Expiry Visual Statuses (HUD & Glowing Indicators)
    materials['status_fresh'] = get_or_create_material("Mat_Status_Fresh", (0.1, 0.85, 0.25, 1.0), emission_color=(0.1, 0.95, 0.25, 1.0), emission_strength=2.5)
    materials['status_warning'] = get_or_create_material("Mat_Status_Warning", (0.98, 0.75, 0.05, 1.0), emission_color=(1.0, 0.8, 0.0, 1.0), emission_strength=3.0)
    materials['status_expired'] = get_or_create_material("Mat_Status_Expired", (0.95, 0.1, 0.1, 1.0), emission_color=(1.0, 0.1, 0.1, 1.0), emission_strength=3.8)
    
    # Category signs
    materials['sign_food'] = get_or_create_material("Mat_Sign_Food", (0.12, 0.65, 0.22, 1.0), roughness=0.25)
    materials['sign_dairy'] = get_or_create_material("Mat_Sign_Dairy", (0.15, 0.55, 0.85, 1.0), roughness=0.25)
    materials['sign_pantry'] = get_or_create_material("Mat_Sign_Pantry", (0.85, 0.45, 0.12, 1.0), roughness=0.25)
    materials['sign_electronics'] = get_or_create_material("Mat_Sign_Electronics", (0.1, 0.35, 0.82, 1.0), roughness=0.25)
    materials['sign_clothing'] = get_or_create_material("Mat_Sign_Clothing", (0.65, 0.2, 0.6, 1.0), roughness=0.25)
    materials['sign_hazardous'] = get_or_create_material("Mat_Sign_Hazardous", (0.9, 0.2, 0.1, 1.0), roughness=0.25)

    # Product Materials - Produce
    materials['prod_apple'] = get_or_create_material("Mat_Prod_Apple", (0.88, 0.08, 0.08, 1.0), roughness=0.22)
    materials['prod_orange'] = get_or_create_material("Mat_Prod_Orange", (0.98, 0.46, 0.04, 1.0), roughness=0.38)
    materials['prod_banana'] = get_or_create_material("Mat_Prod_Banana", (0.98, 0.86, 0.12, 1.0), roughness=0.32)
    materials['prod_tomato'] = get_or_create_material("Mat_Prod_Tomato", (0.92, 0.14, 0.10, 1.0), roughness=0.18)
    materials['prod_stem'] = get_or_create_material("Mat_Prod_Stem", (0.22, 0.42, 0.12, 1.0), roughness=0.5)

    # Product Materials - Dairy & Beverages
    materials['prod_milk'] = get_or_create_material("Mat_Prod_Milk", (0.95, 0.96, 0.98, 1.0), roughness=0.28)
    materials['prod_milk_cap'] = get_or_create_material("Mat_Prod_MilkCap", (0.1, 0.45, 0.85, 1.0), roughness=0.2)
    materials['prod_juice'] = get_or_create_material("Mat_Prod_Juice", (0.95, 0.42, 0.08, 1.0), roughness=0.15)
    materials['prod_juice_bottle'] = get_or_create_material("Mat_Prod_JuiceBottle", (0.9, 0.95, 1.0, 1.0), roughness=0.08, alpha=0.5)

    # Product Materials - Packaged & Bakery
    materials['prod_cereal'] = get_or_create_material("Mat_Prod_Cereal", (0.88, 0.40, 0.15, 1.0), roughness=0.45)
    materials['prod_bread'] = get_or_create_material("Mat_Prod_Bread", (0.82, 0.58, 0.32, 1.0), roughness=0.6)
    materials['prod_bread_bag'] = get_or_create_material("Mat_Prod_BreadBag", (0.92, 0.92, 0.95, 1.0), roughness=0.2, alpha=0.65)

    # Product Materials - Electronics
    materials['prod_phone'] = get_or_create_material("Mat_Prod_Phone", (0.12, 0.13, 0.15, 1.0), roughness=0.08, metallic=0.92)
    materials['prod_phone_screen'] = get_or_create_material("Mat_Prod_PhoneScreen", (0.02, 0.05, 0.1, 1.0), emission_color=(0.15, 0.5, 0.9, 1.0), emission_strength=1.5)
    materials['prod_laptop'] = get_or_create_material("Mat_Prod_Laptop", (0.75, 0.76, 0.78, 1.0), roughness=0.18, metallic=0.88)
    materials['prod_headphone'] = get_or_create_material("Mat_Prod_Headphone", (0.15, 0.15, 0.18, 1.0), roughness=0.25, metallic=0.6)
    materials['prod_battery'] = get_or_create_material("Mat_Prod_Battery", (0.95, 0.75, 0.05, 1.0), roughness=0.25, metallic=0.7)

    # Product Materials - Clothing
    materials['prod_shirt_blue'] = get_or_create_material("Mat_Prod_ShirtBlue", (0.18, 0.42, 0.72, 1.0), roughness=0.85)
    materials['prod_shirt_red'] = get_or_create_material("Mat_Prod_ShirtRed", (0.75, 0.18, 0.22, 1.0), roughness=0.85)
    materials['prod_trousers'] = get_or_create_material("Mat_Prod_Trousers", (0.15, 0.18, 0.24, 1.0), roughness=0.8)
    materials['prod_shoe_box'] = get_or_create_material("Mat_Prod_ShoeBox", (0.85, 0.45, 0.20, 1.0), roughness=0.4)

    # Product Materials - Hazardous & Chemical
    materials['prod_chem_bottle'] = get_or_create_material("Mat_Prod_ChemBottle", (0.92, 0.15, 0.15, 1.0), roughness=0.25)
    materials['prod_chem_spray'] = get_or_create_material("Mat_Prod_ChemSpray", (0.95, 0.85, 0.05, 1.0), roughness=0.25)
    materials['prod_pesticide'] = get_or_create_material("Mat_Prod_Pesticide", (0.15, 0.65, 0.25, 1.0), roughness=0.3)

    return materials
