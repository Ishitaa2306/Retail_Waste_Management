"""
Exact 1-to-1 Supermarket Scene Generator Matching Reference Image f796652b
- Cutaway isometric view from front-left
- 3 Oval/capsule gondolas with top loop signage
- 1 Straight gondola on the left aisle with top signage
- Sloped tiered produce display tables + watermelon & melon crates
- Self-checkout kiosks with touchscreen monitors on left
- Turnstiles / security barriers and traditional red-trim checkout counters
- Back perimeter refrigerated multi-door dairy/drink display cases with glowing headers
- Back wall with roll-up storage shutter, service doors, and upper backroom mezzanine storage
- Two square structural support pillars with dark capital blocks
- Glossy checkered floor tiles reflecting ambient lights
"""

import bpy
import bmesh
import math
import random
import os

def build_reference_supermarket():
    print("[SUPERMARKET_1TO1] Building exact reference model...")
    
    # 1. Clean scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for col in [bpy.data.meshes, bpy.data.materials, bpy.data.textures, bpy.data.lights, bpy.data.cameras]:
        for item in col:
            col.remove(item)

    # 2. Materials
    def make_mat(name, color, roughness=0.3, metallic=0.0, emission=None, emission_strength=1.0):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        b = mat.node_tree.nodes.get('Principled BSDF')
        if b:
            b.inputs['Base Color'].default_value = color
            b.inputs['Roughness'].default_value = roughness
            b.inputs['Metallic'].default_value = metallic
            if emission:
                if 'Emission Color' in b.inputs:
                    b.inputs['Emission Color'].default_value = emission
                elif 'Emission' in b.inputs:
                    b.inputs['Emission'].default_value = emission
                if 'Emission Strength' in b.inputs:
                    b.inputs['Emission Strength'].default_value = emission_strength
        mat.diffuse_color = color
        return mat

    mats = {
        'floor': make_mat('Mat_Floor', (0.92, 0.94, 0.96, 1.0), roughness=0.12),
        'wall_beige': make_mat('Mat_Wall_Beige', (0.88, 0.86, 0.80, 1.0), roughness=0.6),
        'wall_trim': make_mat('Mat_Wall_Trim', (0.2, 0.22, 0.24, 1.0), roughness=0.35),
        'fixture_white': make_mat('Mat_Fixture_White', (0.96, 0.96, 0.97, 1.0), roughness=0.25),
        'metal_dark': make_mat('Mat_Metal_Dark', (0.16, 0.17, 0.19, 1.0), roughness=0.35, metallic=0.8),
        'glass': make_mat('Mat_Glass', (0.92, 0.96, 1.0, 0.3), roughness=0.05),
        'checkout_white': make_mat('Mat_Checkout_White', (0.94, 0.94, 0.95, 1.0), roughness=0.25),
        'checkout_red': make_mat('Mat_Checkout_Red', (0.85, 0.1, 0.1, 1.0), roughness=0.25),
        'checkout_belt': make_mat('Mat_Checkout_Belt', (0.12, 0.12, 0.14, 1.0), roughness=0.7),
        'kiosk_dark': make_mat('Mat_Kiosk_Dark', (0.15, 0.16, 0.18, 1.0), roughness=0.2),
        'kiosk_screen': make_mat('Mat_Kiosk_Screen', (0.05, 0.55, 0.9, 1.0), emission=(0.1, 0.65, 1.0, 1.0), emission_strength=3.5),
        'wood_light': make_mat('Mat_Wood_Light', (0.78, 0.60, 0.40, 1.0), roughness=0.5),
        'pillar_body': make_mat('Mat_Pillar_Body', (0.88, 0.86, 0.80, 1.0), roughness=0.5),
        'pillar_cap': make_mat('Mat_Pillar_Cap', (0.22, 0.24, 0.26, 1.0), roughness=0.3),
        'header_glow': make_mat('Mat_Header_Glow', (0.95, 0.98, 1.0, 1.0), emission=(0.95, 0.98, 1.0, 1.0), emission_strength=2.0),
        # Diverse Product facings
        'p_red': make_mat('Mat_P_Red', (0.85, 0.08, 0.08, 1.0), roughness=0.25),
        'p_orange': make_mat('Mat_P_Orange', (0.95, 0.45, 0.04, 1.0), roughness=0.25),
        'p_yellow': make_mat('Mat_P_Yellow', (0.95, 0.82, 0.08, 1.0), roughness=0.25),
        'p_green': make_mat('Mat_P_Green', (0.12, 0.72, 0.18, 1.0), roughness=0.25),
        'p_cyan': make_mat('Mat_P_Cyan', (0.08, 0.80, 0.85, 1.0), roughness=0.25),
        'p_blue': make_mat('Mat_P_Blue', (0.12, 0.45, 0.88, 1.0), roughness=0.25),
        'p_purple': make_mat('Mat_P_Purple', (0.58, 0.15, 0.68, 1.0), roughness=0.25),
        'p_white': make_mat('Mat_P_White', (0.95, 0.95, 0.98, 1.0), roughness=0.25),
        'p_brown': make_mat('Mat_P_Brown', (0.45, 0.28, 0.14, 1.0), roughness=0.4),
        'melon_dark': make_mat('Mat_Melon_Dark', (0.12, 0.38, 0.12, 1.0), roughness=0.35),
        'melon_stripe': make_mat('Mat_Melon_Stripe', (0.35, 0.75, 0.2, 1.0), roughness=0.35),
    }

    # Setup floor procedural tile grid
    fnodes = mats['floor'].node_tree.nodes
    fnodes.clear()
    tc = fnodes.new('ShaderNodeTexCoord')
    tm = fnodes.new('ShaderNodeMapping')
    tm.inputs['Scale'].default_value = (40.0, 40.0, 1.0)
    tchk = fnodes.new('ShaderNodeTexChecker')
    tchk.inputs['Color1'].default_value = (0.95, 0.96, 0.98, 1.0)
    tchk.inputs['Color2'].default_value = (0.86, 0.88, 0.92, 1.0)
    bsdf = fnodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Roughness'].default_value = 0.14
    fout = fnodes.new('ShaderNodeOutputMaterial')
    flinks = mats['floor'].node_tree.links
    flinks.new(tc.outputs['UV'], tm.inputs['Vector'])
    flinks.new(tm.outputs['Vector'], tchk.inputs['Vector'])
    flinks.new(tchk.outputs['Color'], bsdf.inputs['Base Color'])
    flinks.new(bsdf.outputs[0], fout.inputs[0])

    # Helper mesh box
    def add_box(name, size, loc, mat, col):
        sx, sy, sz = size
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(sx, sy, sz), verts=bm.verts)
        bmesh.ops.translate(bm, vec=(0, 0, sz/2.0), verts=bm.verts)
        me = bpy.data.meshes.new(name+'_Mesh')
        bm.to_mesh(me)
        bm.free()
        if mat:
            me.materials.append(mat)
        ob = bpy.data.objects.new(name, me)
        ob.location = loc
        col.objects.link(ob)
        return ob

    # Collections
    c_arch = bpy.data.collections.new('01_Architecture')
    c_fixt = bpy.data.collections.new('02_Fixtures')
    c_prod = bpy.data.collections.new('03_Products')
    c_chk  = bpy.data.collections.new('04_Checkouts')
    c_cam  = bpy.data.collections.new('05_Cameras')
    c_lite = bpy.data.collections.new('06_Lighting')
    for c in [c_arch, c_fixt, c_prod, c_chk, c_cam, c_lite]:
        bpy.context.scene.collection.children.link(c)

    # 3. FLOOR & WALLS (Open Cutaway Perspective)
    # Main store floor
    add_box('Store_Floor', (24.0, 24.0, 0.2), (0, 0, -0.2), mats['floor'], c_arch)
    
    # Back Wall (North Wall at Y = 12.0)
    add_box('Back_Wall', (24.0, 0.4, 4.8), (0, 12.0, 0), mats['wall_beige'], c_arch)
    add_box('Back_Wall_Baseboard', (24.0, 0.45, 0.35), (0, 12.0, 0), mats['wall_trim'], c_arch)
    
    # Right Wall (East Wall at X = 12.0)
    add_box('Right_Wall', (0.4, 24.0, 4.8), (12.0, 0, 0), mats['wall_beige'], c_arch)
    add_box('Right_Wall_Baseboard', (0.45, 24.0, 0.35), (12.0, 0, 0), mats['wall_trim'], c_arch)

    # Backroom Doors & Garage Roll-up Shutter
    add_box('Warehouse_Rollup_Door', (3.8, 0.1, 3.2), (-4.5, 11.9, 0), mats['fixture_white'], c_arch)
    add_box('Back_Service_Door_L', (1.8, 0.08, 2.7), (-8.8, 11.9, 0), mats['fixture_white'], c_arch)
    add_box('Back_Service_Door_R', (1.8, 0.08, 2.7), (4.8, 11.9, 0), mats['fixture_white'], c_arch)

    # Backroom Mezzanine Racks visible through open upper sections
    for rx in [-9.0, -6.5, -4.0, 5.0]:
        add_box(f'Mezzanine_Rack_{rx}', (2.0, 0.9, 1.6), (rx, 13.5, 0), mats['metal_dark'], c_arch)

    # Front Glass Window Wall with black structural mullions
    for mx in range(-12, 13, 3):
        add_box(f'Mullion_V_{mx}', (0.14, 0.14, 3.4), (mx, -12.0, 0), mats['metal_dark'], c_arch)
    add_box('Mullion_H_Mid', (24.0, 0.14, 0.14), (0, -12.0, 1.7), mats['metal_dark'], c_arch)
    add_box('Mullion_H_Top', (24.0, 0.14, 0.14), (0, -12.0, 3.4), mats['metal_dark'], c_arch)
    add_box('Front_Glass_Panels', (23.8, 0.04, 3.3), (0, -12.0, 0.1), mats['glass'], c_arch)

    # Two Square Architectural Columns with dark accents
    # Column 1 (Left foreground) & Column 2 (Right foreground)
    for col_name, cx, cy in [('Pillar_Left', -4.2, -4.5), ('Pillar_Right', 6.8, -3.2)]:
        add_box(f'{col_name}_Base', (0.85, 0.85, 0.3), (cx, cy, 0), mats['pillar_cap'], c_arch)
        add_box(f'{col_name}_Shaft', (0.75, 0.75, 3.8), (cx, cy, 0.3), mats['pillar_body'], c_arch)
        add_box(f'{col_name}_Cap', (0.82, 0.82, 0.7), (cx, cy, 4.1), mats['pillar_cap'], c_arch)

    # 4. THREE ROUNDED CAPSULE OVAL GONDOLAS (Central Store Fixtures)
    # In the reference image, there are 3 distinct stadium-oval gondolas running parallel
    capsule_positions = [
        ('Capsule_1', -0.5, 0.8, -15),
        ('Capsule_2', 3.2, 3.2, -15),
        ('Capsule_3', 6.8, 5.6, -15)
    ]
    
    prod_colors = [
        mats['p_yellow'], mats['p_red'], mats['p_green'], mats['p_cyan'],
        mats['p_orange'], mats['p_blue'], mats['p_purple'], mats['p_brown']
    ]

    for cname, cx, cy, rot_deg in capsule_positions:
        # Create stadium oval fixture using bmesh
        bm = bmesh.new()
        # Central spine
        bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(2.6, 1.1, 2.0), verts=bm.verts)
        bmesh.ops.translate(bm, vec=(0, 0, 1.0), verts=bm.verts)
        # End cylinders
        bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=0.55, radius2=0.55, depth=2.0)
        for v in bm.verts[-32:]:
            v.co.x += 1.3
            v.co.z += 1.0
        bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=0.55, radius2=0.55, depth=2.0)
        for v in bm.verts[-32:]:
            v.co.x -= 1.3
            v.co.z += 1.0
            
        me = bpy.data.meshes.new(f'{cname}_Body_Mesh')
        bm.to_mesh(me)
        bm.free()
        me.materials.append(mats['fixture_white'])
        ob_capsule = bpy.data.objects.new(f'{cname}_Body', me)
        ob_capsule.location = (cx, cy, 0)
        ob_capsule.rotation_euler.z = math.radians(rot_deg)
        c_fixt.objects.link(ob_capsule)

        # Overhead White Oval Canopy Loop Ring
        bm_ring = bmesh.new()
        bmesh.ops.create_cube(bm_ring, size=1.0)
        bmesh.ops.scale(bm_ring, vec=(3.6, 1.35, 0.22), verts=bm_ring.verts)
        bmesh.ops.translate(bm_ring, vec=(0, 0, 2.05), verts=bm_ring.verts)
        me_ring = bpy.data.meshes.new(f'{cname}_Ring_Mesh')
        bm_ring.to_mesh(me_ring)
        bm_ring.free()
        me_ring.materials.append(mats['fixture_white'])
        ob_ring = bpy.data.objects.new(f'{cname}_Ring', me_ring)
        ob_ring.location = (cx, cy, 0)
        ob_ring.rotation_euler.z = math.radians(rot_deg)
        c_fixt.objects.link(ob_ring)

        # Stock products across all 5 tiers of the capsule gondola
        cos_r = math.cos(math.radians(rot_deg))
        sin_r = math.sin(math.radians(rot_deg))
        
        for ti in range(5):
            tz = 0.25 + ti * 0.38
            # Front facing items
            for pi in range(9):
                local_x = -1.2 + pi * 0.3
                local_y = -0.6
                gx = cx + (local_x * cos_r - local_y * sin_r)
                gy = cy + (local_x * sin_r + local_y * cos_r)
                c_mat = prod_colors[(ti + pi) % len(prod_colors)]
                add_box(f'{cname}_P_F_{ti}_{pi}', (0.16, 0.16, 0.26), (gx, gy, tz), c_mat, c_prod)
            # Back facing items
            for pi in range(9):
                local_x = -1.2 + pi * 0.3
                local_y = 0.6
                gx = cx + (local_x * cos_r - local_y * sin_r)
                gy = cy + (local_x * sin_r + local_y * cos_r)
                c_mat = prod_colors[(ti + pi + 3) % len(prod_colors)]
                add_box(f'{cname}_P_B_{ti}_{pi}', (0.16, 0.16, 0.26), (gx, gy, tz), c_mat, c_prod)

    # 5. WALL REFRIGERATION UNITS & GONDOLAS
    # Back Center: 6-Door Glass Refrigerated Case (Drinks/Dairy)
    add_box('Fridge_Main_Body', (6.5, 0.85, 2.6), (0.2, 9.8, 0), mats['fixture_white'], c_fixt)
    add_box('Fridge_Glow_Header', (6.5, 0.88, 0.35), (0.2, 9.8, 2.6), mats['header_glow'], c_fixt)
    for di in range(6):
        dx = -2.5 + di * 1.0 + 0.5
        add_box(f'Fridge_Door_{di}', (0.94, 0.04, 2.15), (dx, 9.35, 0.35), mats['glass'], c_fixt)
        for ti in range(5):
            tz = 0.4 + ti * 0.4
            for bi in range(4):
                bx = dx - 0.3 + bi * 0.2
                c_mat = prod_colors[(di + ti + bi) % len(prod_colors)]
                add_box(f'Drink_{di}_{ti}_{bi}', (0.12, 0.12, 0.24), (bx, 9.6, tz), c_mat, c_prod)

    # Back-Left Wall Unit (Packaged Goods / Cereals)
    add_box('Wall_Unit_Left', (5.5, 0.75, 2.6), (-6.5, 9.8, 0), mats['fixture_white'], c_fixt)
    add_box('Wall_Unit_Left_Header', (5.6, 0.78, 0.35), (-6.5, 9.8, 2.6), mats['fixture_white'], c_fixt)
    for ti in range(5):
        tz = 0.3 + ti * 0.42
        for pi in range(15):
            px = -8.8 + pi * 0.34
            add_box(f'WUL_Prod_{ti}_{pi}', (0.18, 0.14, 0.28), (px, 9.6, tz), mats['p_yellow'] if ti%2==0 else mats['p_red'], c_prod)

    # Right Wall Long Gondola Units (Apparel / Home)
    add_box('Right_Wall_Gondola', (0.75, 7.5, 2.6), (9.8, 6.5, 0), mats['fixture_white'], c_fixt)
    add_box('Right_Wall_Gondola_Header', (0.78, 7.6, 0.35), (9.8, 6.5, 2.6), mats['fixture_white'], c_fixt)
    for ti in range(5):
        tz = 0.3 + ti * 0.42
        for pi in range(18):
            py = 3.2 + pi * 0.36
            add_box(f'RWG_Prod_{ti}_{pi}', (0.15, 0.2, 0.26), (9.6, py, tz), mats['p_purple'] if ti%2==0 else mats['p_green'], c_prod)

    # Foreground Left Aisle Straight Gondola (Full Facings)
    add_box('Aisle_Gondola_Front_Left', (1.2, 5.2, 2.0), (-9.2, -1.5, 0), mats['fixture_white'], c_fixt)
    add_box('Aisle_Gondola_FL_Header', (1.25, 5.3, 0.25), (-9.2, -1.5, 2.0), mats['fixture_white'], c_fixt)
    for ti in range(5):
        tz = 0.25 + ti * 0.36
        for yi in range(14):
            py = -3.8 + yi * 0.35
            add_box(f'FL_Prod_{ti}_{yi}', (0.22, 0.14, 0.25), (-8.7, py, tz), mats['p_cyan'] if ti%2==0 else mats['p_orange'], c_prod)

    # Far Left Wall Dairy Cooler Unit
    add_box('Far_Left_Cooler', (0.75, 3.6, 2.4), (-11.2, 6.2, 0), mats['fixture_white'], c_fixt)
    add_box('Far_Left_Cooler_Header', (0.8, 3.7, 0.3), (-11.2, 6.2, 2.4), mats['checkout_red'], c_fixt)

    # 6. CENTRAL FRESH PRODUCE DISPLAY TABLES & CRATES
    # Sloped wooden tables with orange/apple pyramids
    add_box('Produce_Table_Main', (2.4, 1.8, 0.85), (-3.8, 2.2, 0), mats['wood_light'], c_fixt)
    add_box('Produce_Table_Slope', (2.2, 1.6, 0.35), (-3.8, 2.2, 0.85), mats['wood_light'], c_fixt)
    add_box('Produce_Price_Pole', (0.04, 0.04, 0.7), (-3.8, 2.8, 1.1), mats['metal_dark'], c_fixt)
    add_box('Produce_Price_Board', (0.55, 0.04, 0.35), (-3.8, 2.8, 1.8), mats['fixture_white'], c_fixt)
    for ox in [-0.55, 0.55]:
        for oy in [-0.4, 0.4]:
            add_box(f'Produce_Fruit_{ox}_{oy}', (0.65, 0.55, 0.25), (-3.8 + ox, 2.2 + oy, 1.2), mats['p_orange'] if ox<0 else mats['p_red'], c_prod)

    # Produce Stand 2 (Citrus & Lemons)
    add_box('Produce_Stand_2', (2.2, 1.5, 0.75), (-2.0, -1.8, 0), mats['wood_light'], c_fixt)
    add_box('Produce_S2_Top', (2.0, 1.3, 0.25), (-2.0, -1.8, 0.75), mats['wood_light'], c_fixt)
    for ox in [-0.45, 0.45]:
        add_box(f'Fruit_Heap_{ox}', (0.6, 0.9, 0.22), (-2.0 + ox, -1.8, 1.0), mats['p_yellow'] if ox<0 else mats['p_red'], c_prod)

    # Standalone Wooden Fruit Crates
    # Crate 1: Watermelons (spheres)
    add_box('Watermelon_Crate', (1.3, 1.3, 0.65), (-6.5, -1.8, 0), mats['wood_light'], c_fixt)
    bm_wm = bmesh.new()
    bmesh.ops.create_uvsphere(bm_wm, u_segments=14, v_segments=10, radius=0.15)
    me_wm = bpy.data.meshes.new('Watermelon_Mesh')
    bm_wm.to_mesh(me_wm)
    bm_wm.free()
    me_wm.materials.append(mats['melon_dark'])
    for wx in [-0.28, 0.28]:
        for wy in [-0.28, 0.28]:
            ob_w = bpy.data.objects.new(f'Watermelon_{wx}_{wy}', me_wm)
            ob_w.location = (-6.5 + wx, -1.8 + wy, 0.72)
            c_prod.objects.link(ob_w)

    # Crate 2: Citrus melons
    add_box('Citrus_Crate', (1.3, 1.3, 0.65), (-5.0, -5.5, 0), mats['wood_light'], c_fixt)
    for cx in [-0.28, 0.0, 0.28]:
        for cy in [-0.28, 0.0, 0.28]:
            ob_c = bpy.data.objects.new(f'Citrus_{cx}_{cy}', me_wm)
            ob_c.location = (-5.0 + cx, -5.5 + cy, 0.72)
            ob_c.data.materials.clear()
            ob_c.data.materials.append(mats['p_orange'])
            c_prod.objects.link(ob_c)

    # 7. FRONT CHECKOUT COUNTERS, GATES & TOUCHSCREEN KIOSKS
    # Traditional Cashier Counters with red borders & conveyor belts
    for ci, cx in enumerate([3.5, 7.5]):
        add_box(f'Checkout_Desk_{ci}', (2.5, 1.4, 0.85), (cx, -7.5, 0), mats['checkout_white'], c_chk)
        add_box(f'Checkout_Belt_{ci}', (1.7, 0.55, 0.05), (cx - 0.2, -7.5, 0.85), mats['checkout_belt'], c_chk)
        add_box(f'Checkout_RedTrim_{ci}', (2.55, 1.45, 0.06), (cx, -7.5, 0.82), mats['checkout_red'], c_chk)
        add_box(f'Checkout_ScreenStand_{ci}', (0.08, 0.08, 0.4), (cx + 0.8, -7.2, 0.85), mats['metal_dark'], c_chk)
        add_box(f'Checkout_Screen_{ci}', (0.35, 0.05, 0.28), (cx + 0.8, -7.2, 1.25), mats['kiosk_screen'], c_chk)

    # Self-Checkout Touchscreen Kiosks (Black pedestals angled screens)
    for ki in range(5):
        kx = -10.8 + ki * 1.25
        add_box(f'SelfCheckout_Base_{ki}', (0.55, 0.55, 0.95), (kx, -8.8, 0), mats['kiosk_dark'], c_chk)
        scr = add_box(f'SelfCheckout_Screen_{ki}', (0.42, 0.06, 0.38), (kx, -8.8, 1.05), mats['kiosk_screen'], c_chk)
        scr.rotation_euler.x = math.radians(-20)

    # Security Turnstiles / Gates
    for gi, gx in enumerate([0.2, 1.5]):
        add_box(f'Gate_Post_{gi}', (0.14, 0.14, 1.1), (gx, -8.2, 0), mats['fixture_white'], c_chk)
        add_box(f'Gate_Arm_{gi}', (0.85, 0.04, 0.28), (gx + 0.42, -8.2, 0.7), mats['glass'], c_chk)
        add_box(f'Gate_StopSign_{gi}', (0.16, 0.05, 0.16), (gx + 0.42, -8.2, 0.7), mats['checkout_red'], c_chk)

    # 8. LIGHTING & CAMERAS
    # Sunlight fill
    sun_data = bpy.data.lights.new('Sun_Fill', type='SUN')
    sun_data.energy = 2.6
    sun_data.color = (0.98, 0.98, 1.0)
    sun_ob = bpy.data.objects.new('Sun_Fill', sun_data)
    sun_ob.rotation_euler = (math.radians(50), math.radians(20), math.radians(-30))
    c_lite.objects.link(sun_ob)

    # Ambient overhead fill
    for lx in [-6.0, 0.0, 6.0]:
        for ly in [-4.0, 2.0, 8.0]:
            l_data = bpy.data.lights.new(f'Ceil_Light_{lx}_{ly}', type='AREA')
            l_data.energy = 380.0
            l_data.size = 3.5
            l_ob = bpy.data.objects.new(f'Ceil_Light_{lx}_{ly}', l_data)
            l_ob.location = (lx, ly, 7.5)
            c_lite.objects.link(l_ob)

    # Main Reference Isometric Camera
    # High cutaway perspective matching the user's reference image exactly
    cam_data = bpy.data.cameras.new('Cam_Reference_Isometric_Data')
    cam_data.type = 'PERSP'
    cam_data.lens = 28.0
    cam_ob = bpy.data.objects.new('Cam_Reference_Isometric', cam_data)
    cam_ob.location = (-13.5, -19.5, 17.5)
    cam_ob.rotation_euler = (math.radians(51.5), 0, math.radians(-37.5))
    c_cam.objects.link(cam_ob)
    bpy.context.scene.camera = cam_ob

    # Save blend file
    save_path = os.path.abspath('Retail_Waste_Management.blend')
    bpy.ops.wm.save_as_mainfile(filepath=save_path)
    print(f"[SUPERMARKET_1TO1] Complete! Total scene objects: {len(bpy.data.objects)}. Saved to {save_path}")

if __name__ == '__main__':
    build_reference_supermarket()
