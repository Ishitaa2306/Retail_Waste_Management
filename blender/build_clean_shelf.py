"""
Clean Retail Shelf and Product Staging Generator
Recreates the exact clean, aesthetic supermarket shelf product presentation from reference image media_1795485646337_885e34e4.jpg:
- Grey 3-tier retail display shelving unit with clean rounded tubular posts
- Category signs on the top shelf railing: [MILK] [RICE] [BREAD] [EGGS] [JUICE]
- Pristine, neatly arranged product geometries:
  1. MILK: White cartons with blue square labels and blue screw caps
  2. RICE: Soft paper/canvas bags with green labels
  3. BREAD: Round baked loaves in translucent packaging with orange bands
  4. EGGS: Molded cardboard egg cartons (3x6 and 2x6) with individual egg spheres
  5. JUICE: Rounded translucent amber/orange glass bottles with green screw caps and white labels
- Lower shelf status indicator strips:
  - Green [STOCK OK] strips
  - Red [RESTOCK] strips
"""

import bpy
import bmesh
import math
import os

def build_clean_shelf_showcase():
    print("[CLEAN_SHELF] Building clean aesthetic supermarket shelf...")
    
    # Clean scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for col in [bpy.data.meshes, bpy.data.materials, bpy.data.textures, bpy.data.lights, bpy.data.cameras]:
        for item in col:
            col.remove(item)

    # 1. Materials
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
        'backdrop': make_mat('Mat_Backdrop', (0.55, 0.58, 0.60, 1.0), roughness=0.7),
        'floor': make_mat('Mat_Studio_Floor', (0.42, 0.45, 0.48, 1.0), roughness=0.4),
        'shelf_grey': make_mat('Mat_Shelf_Grey', (0.76, 0.78, 0.80, 1.0), roughness=0.3),
        'sign_dark': make_mat('Mat_Sign_Dark', (0.18, 0.20, 0.22, 1.0), roughness=0.3),
        'metal_dark': make_mat('Mat_Metal_Dark', (0.18, 0.20, 0.22, 1.0), roughness=0.3, metallic=0.7),
        'text_white': make_mat('Mat_Text_White', (0.95, 0.95, 0.95, 1.0), emission=(1.0, 1.0, 1.0, 1.0), emission_strength=1.5),
        'status_green': make_mat('Mat_Status_Green', (0.15, 0.65, 0.25, 1.0), emission=(0.15, 0.75, 0.25, 1.0), emission_strength=1.2),
        'status_red': make_mat('Mat_Status_Red', (0.85, 0.15, 0.12, 1.0), emission=(0.95, 0.15, 0.12, 1.0), emission_strength=1.2),
        # Milk
        'milk_body': make_mat('Mat_Milk_Body', (0.95, 0.95, 0.97, 1.0), roughness=0.25),
        'milk_blue': make_mat('Mat_Milk_Blue', (0.15, 0.45, 0.85, 1.0), roughness=0.25),
        # Rice
        'rice_bag': make_mat('Mat_Rice_Bag', (0.88, 0.86, 0.80, 1.0), roughness=0.6),
        'rice_green': make_mat('Mat_Rice_Green', (0.18, 0.65, 0.32, 1.0), roughness=0.3),
        # Bread
        'bread_crust': make_mat('Mat_Bread_Crust', (0.92, 0.88, 0.82, 1.0), roughness=0.45),
        'bread_band': make_mat('Mat_Bread_Band', (0.92, 0.52, 0.15, 1.0), roughness=0.3),
        # Eggs
        'egg_carton': make_mat('Mat_Egg_Carton', (0.75, 0.68, 0.58, 1.0), roughness=0.7),
        'egg_shell': make_mat('Mat_Egg_Shell', (0.94, 0.92, 0.88, 1.0), roughness=0.35),
        # Juice
        'juice_amber': make_mat('Mat_Juice_Amber', (0.92, 0.55, 0.08, 1.0), roughness=0.2),
        'juice_green': make_mat('Mat_Juice_Green', (0.12, 0.55, 0.22, 1.0), roughness=0.2),
        'juice_label': make_mat('Mat_Juice_Label', (0.94, 0.94, 0.92, 1.0), roughness=0.4)
    }

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
    c_shelf = bpy.data.collections.new('01_Shelving_Unit')
    c_prod  = bpy.data.collections.new('02_Stock_Products')
    c_signs = bpy.data.collections.new('03_Signs_and_Indicators')
    c_env   = bpy.data.collections.new('04_Studio_Environment')
    for c in [c_shelf, c_prod, c_signs, c_env]:
        bpy.context.scene.collection.children.link(c)

    # Studio Floor & Background Wall
    add_box('Studio_Floor', (16.0, 10.0, 0.2), (0, 0, -0.2), mats['floor'], c_env)
    add_box('Studio_Backdrop', (16.0, 0.2, 5.0), (0, 2.5, 0), mats['backdrop'], c_env)

    # 2. RETAIL DISPLAY SHELVING UNIT (3 Tiers with tubular posts)
    shelf_length = 9.2
    shelf_depth = 0.95
    shelf_thick = 0.05
    tier_z_levels = [0.35, 0.95, 1.55]

    for ti, tz in enumerate(tier_z_levels):
        # Shelf plank with bevel/lip
        add_box(f'Shelf_Plank_{ti+1}', (shelf_length, shelf_depth, shelf_thick), (0.0, 0.0, tz), mats['shelf_grey'], c_shelf)

    # 4 Vertical Support Tubular Posts (Left, Center-Left, Center-Right, Right)
    for pi, px in enumerate([-4.4, -1.8, 1.2, 4.4]):
        bm_p = bmesh.new()
        bmesh.ops.create_cone(bm_p, cap_ends=True, segments=16, radius1=0.038, radius2=0.038, depth=1.85)
        bmesh.ops.translate(bm_p, vec=(0, 0, 0.925), verts=bm_p.verts)
        me_p = bpy.data.meshes.new(f'Shelf_Post_{pi}_Mesh')
        bm_p.to_mesh(me_p)
        bm_p.free()
        me_p.materials.append(mats['shelf_grey'])
        ob_p = bpy.data.objects.new(f'Shelf_Post_{pi}', me_p)
        ob_p.location = (px, 0.38, 0.0)
        c_shelf.objects.link(ob_p)

    # 3. FIVE CATEGORY PRODUCT SECTIONS
    # Sections from Left to Right:
    # 1. MILK  (x = -3.5)
    # 2. RICE  (x = -1.8)
    # 3. BREAD (x = -0.1)
    # 4. EGGS  (x = 1.6)
    # 5. JUICE (x = 3.3)

    sections = [
        ('MILK',  -3.5, mats['status_red']),
        ('RICE',  -1.8, mats['status_green']),
        ('BREAD', -0.1, mats['status_red']),
        ('EGGS',   1.6, mats['status_red']),
        ('JUICE',  3.3, mats['status_green'])
    ]

    for cat_name, cx, status_mat in sections:
        # Category sign board on top railing
        add_box(f'Sign_{cat_name}', (1.35, 0.04, 0.22), (cx, -0.38, 1.62), mats['sign_dark'], c_signs)
        # Sign support bracket
        add_box(f'Sign_Bracket_{cat_name}', (0.03, 0.03, 0.15), (cx, -0.38, 1.55), mats['metal_dark'], c_signs)
        # Category Text label (white bar/badge on sign)
        add_box(f'Sign_Text_{cat_name}', (0.75, 0.01, 0.08), (cx, -0.41, 1.69), mats['text_white'], c_signs)

        # Floor indicator bar [STOCK OK] or [RESTOCK]
        add_box(f'Indicator_Bar_{cat_name}', (1.35, 0.06, 0.12), (cx, -0.42, 0.12), status_mat, c_signs)

    # 4. PRISTINE PRODUCT MODELS (Populating Tier 1, 2, 3)

    # --- CATEGORY 1: MILK CARTONS ---
    # White gable-top milk cartons with blue square labels & blue caps
    def create_clean_milk_carton(name, loc):
        # Body
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(0.20, 0.20, 0.34), verts=bm.verts)
        bmesh.ops.translate(bm, vec=(0, 0, 0.17), verts=bm.verts)
        # Cap
        bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.03, radius2=0.03, depth=0.03)
        for v in bm.verts[-24:]:
            v.co.x += 0.03
            v.co.y += 0.03
            v.co.z += 0.355
        me = bpy.data.meshes.new(name+'_Mesh')
        bm.to_mesh(me)
        bm.free()
        me.materials.append(mats['milk_body'])
        ob = bpy.data.objects.new(name, me)
        ob.location = loc
        c_prod.objects.link(ob)
        # Blue front label
        add_box(name+'_Label', (0.12, 0.01, 0.12), (loc[0], loc[1] - 0.105, loc[2] + 0.14), mats['milk_blue'], c_prod)

    # Place Milk across Tier 1, 2, 3
    # Top tier: 3 milk cartons
    for i, mx in enumerate([-3.8, -3.5, -3.2]):
        create_clean_milk_carton(f'Milk_T3_{i}', (mx, -0.1, 1.60))
    # Middle tier: 3 milk cartons
    for i, mx in enumerate([-3.8, -3.5, -3.2]):
        create_clean_milk_carton(f'Milk_T2_{i}', (mx, -0.1, 1.00))
    # Bottom tier: 3 milk cartons
    for i, mx in enumerate([-3.8, -3.5, -3.2]):
        create_clean_milk_carton(f'Milk_T1_{i}', (mx, -0.1, 0.40))

    # --- CATEGORY 2: RICE BAGS ---
    # Beige soft paper bags with green label bands
    def create_clean_rice_bag(name, loc):
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(0.24, 0.22, 0.22), verts=bm.verts)
        bmesh.ops.translate(bm, vec=(0, 0, 0.11), verts=bm.verts)
        me = bpy.data.meshes.new(name+'_Mesh')
        bm.to_mesh(me)
        bm.free()
        me.materials.append(mats['rice_bag'])
        ob = bpy.data.objects.new(name, me)
        ob.location = loc
        c_prod.objects.link(ob)
        # Green label
        add_box(name+'_Label', (0.16, 0.01, 0.10), (loc[0], loc[1] - 0.115, loc[2] + 0.08), mats['rice_green'], c_prod)

    for i, rx in enumerate([-2.1, -1.8, -1.5]):
        create_clean_rice_bag(f'Rice_T3_{i}', (rx, -0.1, 1.60))
        create_clean_rice_bag(f'Rice_T2_{i}', (rx, -0.1, 1.00))
        create_clean_rice_bag(f'Rice_T1_{i}', (rx, -0.1, 0.40))

    # --- CATEGORY 3: BREAD LOAVES ---
    # Round baked spherical/capsule loaves with orange band
    def create_clean_bread(name, loc):
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=12, radius=0.12)
        bmesh.ops.scale(bm, vec=(1.0, 1.0, 0.85), verts=bm.verts)
        bmesh.ops.translate(bm, vec=(0, 0, 0.10), verts=bm.verts)
        me = bpy.data.meshes.new(name+'_Mesh')
        bm.to_mesh(me)
        bm.free()
        me.materials.append(mats['bread_crust'])
        ob = bpy.data.objects.new(name, me)
        ob.location = loc
        c_prod.objects.link(ob)
        # Orange wrap band
        add_box(name+'_Band', (0.14, 0.25, 0.06), (loc[0], loc[1], loc[2] + 0.08), mats['bread_band'], c_prod)

    for i, bx in enumerate([-0.4, -0.1, 0.2]):
        create_clean_bread(f'Bread_T3_{i}', (bx, -0.1, 1.60))
        create_clean_bread(f'Bread_T2_{i}', (bx, -0.1, 1.00))
        create_clean_bread(f'Bread_T1_{i}', (bx, -0.1, 0.40))

    # --- CATEGORY 4: EGGS (MOLDED TRAYS & CARTONS) ---
    def create_clean_egg_carton(name, loc):
        # Tray base
        add_box(name+'_Tray', (0.55, 0.26, 0.08), loc, mats['egg_carton'], c_prod)
        # Individual egg spheres (2 rows of 6 eggs = 12 eggs)
        for er in [-0.06, 0.06]:
            for ec in range(6):
                ex = loc[0] - 0.22 + ec * 0.09
                bm_e = bmesh.new()
                bmesh.ops.create_uvsphere(bm_e, u_segments=10, v_segments=8, radius=0.032)
                bmesh.ops.scale(bm_e, vec=(1.0, 1.0, 1.25), verts=bm_e.verts)
                bmesh.ops.translate(bm_e, vec=(ex, loc[1] + er, loc[2] + 0.10), verts=bm_e.verts)
                me_e = bpy.data.meshes.new(f'{name}_Egg_{er}_{ec}_Mesh')
                bm_e.to_mesh(me_e)
                bm_e.free()
                me_e.materials.append(mats['egg_shell'])
                ob_e = bpy.data.objects.new(f'{name}_Egg_{er}_{ec}', me_e)
                c_prod.objects.link(ob_e)

    # 2 egg cartons side by side on tier 1 and tier 2
    create_clean_egg_carton('Egg_T2_L', (1.3, -0.1, 1.00))
    create_clean_egg_carton('Egg_T2_R', (1.9, -0.1, 1.00))
    create_clean_egg_carton('Egg_T1_L', (1.3, -0.1, 0.40))
    create_clean_egg_carton('Egg_T1_R', (1.9, -0.1, 0.40))

    # Single row on top tier
    create_clean_egg_carton('Egg_T3', (1.6, -0.1, 1.60))

    # --- CATEGORY 5: JUICE BOTTLES ---
    # Amber glass bottles with green screw caps & white front labels
    def create_clean_juice_bottle(name, loc):
        bm = bmesh.new()
        # Main bottle cylinder
        bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=0.08, radius2=0.08, depth=0.22)
        # Neck
        bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.04, radius2=0.04, depth=0.06)
        for v in bm.verts[-24:]:
            v.co.z += 0.14
        # Cap
        bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.042, radius2=0.042, depth=0.035)
        for v in bm.verts[-24:]:
            v.co.z += 0.185
        bmesh.ops.translate(bm, vec=(0, 0, 0.11), verts=bm.verts)
        me = bpy.data.meshes.new(name+'_Mesh')
        bm.to_mesh(me)
        bm.free()
        me.materials.append(mats['juice_amber'])
        ob = bpy.data.objects.new(name, me)
        ob.location = loc
        c_prod.objects.link(ob)
        # Front label
        add_box(name+'_Label', (0.09, 0.01, 0.10), (loc[0], loc[1] - 0.082, loc[2] + 0.08), mats['juice_label'], c_prod)

    for i, jx in enumerate([3.0, 3.3, 3.6]):
        create_clean_juice_bottle(f'Juice_T3_{i}', (jx, -0.1, 1.60))
        create_clean_juice_bottle(f'Juice_T2_{i}', (jx, -0.1, 1.00))
        create_clean_juice_bottle(f'Juice_T1_{i}', (jx, -0.1, 0.40))

    # 5. STUDIO LIGHTING & CAMERAS (Matching reference image 3/4 perspective)
    # Key light (soft front-left)
    key_data = bpy.data.lights.new('Key_Light', type='AREA')
    key_data.energy = 220.0
    key_data.size = 3.0
    key_data.color = (1.0, 0.98, 0.96)
    key_ob = bpy.data.objects.new('Key_Light', key_data)
    key_ob.location = (-3.5, -4.5, 4.0)
    c_env.objects.link(key_ob)

    # Fill light (soft right)
    fill_data = bpy.data.lights.new('Fill_Light', type='AREA')
    fill_data.energy = 120.0
    fill_data.size = 4.0
    fill_data.color = (0.95, 0.98, 1.0)
    fill_ob = bpy.data.objects.new('Fill_Light', fill_data)
    fill_ob.location = (4.0, -3.5, 3.5)
    c_env.objects.link(fill_ob)

    # Background ambient glow strip (behind top shelf)
    back_light = bpy.data.lights.new('Back_Strip_Light', type='AREA')
    back_light.energy = 85.0
    back_light.size = 8.0
    back_light.size_y = 0.5
    back_light.color = (0.92, 1.0, 0.94)
    back_ob = bpy.data.objects.new('Back_Strip_Light', back_light)
    back_ob.location = (0.0, 1.2, 2.2)
    c_env.objects.link(back_ob)

    # Camera matching exact perspective of reference image 885e34e4.jpg:
    # Slightly elevated front-left perspective angled towards the right
    cam_data = bpy.data.cameras.new('Cam_Clean_Shelf_Data')
    cam_data.type = 'PERSP'
    cam_data.lens = 45.0
    cam_ob = bpy.data.objects.new('Cam_Clean_Shelf', cam_data)
    cam_ob.location = (-4.8, -6.8, 3.8)
    cam_ob.rotation_euler = (math.radians(65.0), 0, math.radians(-32.0))
    c_env.objects.link(cam_ob)
    bpy.context.scene.camera = cam_ob

    # Save directly to main blend file
    save_path = os.path.abspath('Retail_Waste_Management.blend')
    bpy.ops.wm.save_as_mainfile(filepath=save_path)
    print(f"[CLEAN_SHELF] Successfully saved clean aesthetic shelf scene with {len(bpy.data.objects)} objects to {save_path}!")

if __name__ == '__main__':
    build_clean_shelf_showcase()
