"""
Full Supermarket with Clean Shelves Matching 885e34e4
Replaces all gondola shelves in the supermarket architecture with the exact clean 3-tier shelves:
- Category signage: [MILK], [RICE], [BREAD], [EGGS], [JUICE]
- Real items:
  1. MILK cartons with blue label and cap
  2. RICE paper bags with green label
  3. BREAD round loaves with orange wrapper band
  4. EGGS: Real molded cardboard cartons with 2x6 individual egg spheres!
  5. JUICE: Amber glass bottles with green screw cap and label
- Lower shelf status indicator bars: [STOCK OK] (green) and [RESTOCK] (red)
"""

import bpy
import bmesh
import math
import os

def build_supermarket_with_clean_shelves():
    print("[BUILD] Integrating exact clean shelves into the supermarket...")
    
    p = os.path.abspath('Retail_Waste_Management.blend')
    bpy.ops.wm.open_mainfile(filepath=p)
    
    # Remove old proxy capsule gondolas and their products
    old_objs = [o for o in bpy.data.objects if o.name.startswith('Capsule_') or o.name.startswith('Wall_Unit_') or o.name.startswith('Right_Wall_Gondola') or o.name.startswith('Produce_Fruit_') or o.name.startswith('Fruit_Heap_') or o.name.startswith('Prod_')]
    for o in old_objs:
        bpy.data.objects.remove(o, do_unlink=True)
        
    c_fixt = bpy.data.collections.get('02_Fixtures') or bpy.data.collections.new('02_Fixtures')
    c_prod = bpy.data.collections.get('03_Products') or bpy.data.collections.new('03_Products')
    
    # Helper materials
    def make_mat(name, color, roughness=0.3, metallic=0.0, emission=None, emission_strength=1.0):
        mat = bpy.data.materials.get(name) or bpy.data.materials.new(name=name)
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
        'shelf_grey': make_mat('Mat_Clean_Shelf_Grey', (0.76, 0.78, 0.80, 1.0), roughness=0.3),
        'metal_dark': make_mat('Mat_Clean_Metal_Dark', (0.18, 0.20, 0.22, 1.0), roughness=0.3, metallic=0.7),
        'sign_dark': make_mat('Mat_Clean_Sign_Dark', (0.18, 0.20, 0.22, 1.0), roughness=0.3),
        'text_white': make_mat('Mat_Clean_Text_White', (0.95, 0.95, 0.95, 1.0), emission=(1.0, 1.0, 1.0, 1.0), emission_strength=2.0),
        'status_green': make_mat('Mat_Clean_Status_Green', (0.15, 0.65, 0.25, 1.0), emission=(0.15, 0.75, 0.25, 1.0), emission_strength=1.5),
        'status_red': make_mat('Mat_Clean_Status_Red', (0.85, 0.15, 0.12, 1.0), emission=(0.95, 0.15, 0.12, 1.0), emission_strength=1.5),
        'milk_body': make_mat('Mat_Clean_Milk_Body', (0.95, 0.95, 0.97, 1.0), roughness=0.25),
        'milk_blue': make_mat('Mat_Clean_Milk_Blue', (0.15, 0.45, 0.85, 1.0), roughness=0.25),
        'rice_bag': make_mat('Mat_Clean_Rice_Bag', (0.88, 0.86, 0.80, 1.0), roughness=0.6),
        'rice_green': make_mat('Mat_Clean_Rice_Green', (0.18, 0.65, 0.32, 1.0), roughness=0.3),
        'bread_crust': make_mat('Mat_Clean_Bread_Crust', (0.92, 0.88, 0.82, 1.0), roughness=0.45),
        'bread_band': make_mat('Mat_Clean_Bread_Band', (0.92, 0.52, 0.15, 1.0), roughness=0.3),
        'egg_carton': make_mat('Mat_Clean_Egg_Carton', (0.75, 0.68, 0.58, 1.0), roughness=0.7),
        'egg_shell': make_mat('Mat_Clean_Egg_Shell', (0.94, 0.92, 0.88, 1.0), roughness=0.35),
        'juice_amber': make_mat('Mat_Clean_Juice_Amber', (0.92, 0.55, 0.08, 1.0), roughness=0.2),
        'juice_green': make_mat('Mat_Clean_Juice_Green', (0.12, 0.55, 0.22, 1.0), roughness=0.2),
        'juice_label': make_mat('Mat_Clean_Juice_Label', (0.94, 0.94, 0.92, 1.0), roughness=0.4)
    }

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

    # FUNCTION TO SPAWN THE EXACT CLEAN SHELF UNIT AT ANY AISLE POSITION
    def create_clean_aisle_shelf(prefix, base_loc, rot_z=0):
        # 3 Shelf Tiers
        shelf_len = 8.8
        shelf_dep = 0.85
        shelf_thk = 0.04
        tier_z_rel = [0.25, 0.85, 1.45]
        
        cos_a = math.cos(math.radians(rot_z))
        sin_a = math.sin(math.radians(rot_z))
        
        def to_world(lx, ly, lz):
            wx = base_loc[0] + (lx * cos_a - ly * sin_a)
            wy = base_loc[1] + (lx * sin_a + ly * cos_a)
            wz = base_loc[2] + lz
            return (wx, wy, wz)

        # 3 Planks
        for ti, tz in enumerate(tier_z_rel):
            ob = add_box(f'{prefix}_Plank_{ti+1}', (shelf_len, shelf_dep, shelf_thk), to_world(0, 0, tz), mats['shelf_grey'], c_fixt)
            ob.rotation_euler.z = math.radians(rot_z)
            
        # Support posts
        for px in [-4.2, -1.8, 1.2, 4.2]:
            bm_p = bmesh.new()
            bmesh.ops.create_cone(bm_p, cap_ends=True, segments=12, radius1=0.035, radius2=0.035, depth=1.75)
            bmesh.ops.translate(bm_p, vec=(0, 0, 0.875), verts=bm_p.verts)
            me_p = bpy.data.meshes.new(f'{prefix}_Post_{px}_Mesh')
            bm_p.to_mesh(me_p)
            bm_p.free()
            me_p.materials.append(mats['shelf_grey'])
            ob_p = bpy.data.objects.new(f'{prefix}_Post_{px}', me_p)
            ob_p.location = to_world(px, 0.35, 0)
            ob_p.rotation_euler.z = math.radians(rot_z)
            c_fixt.objects.link(ob_p)

        # 5 Category Sections across the shelf
        sections = [
            ('MILK',  -3.3, mats['status_red']),
            ('RICE',  -1.7, mats['status_green']),
            ('BREAD', -0.1, mats['status_red']),
            ('EGGS',   1.5, mats['status_red']),
            ('JUICE',  3.1, mats['status_green'])
        ]
        
        for cat_name, cx, status_mat in sections:
            # Top sign
            ob_s = add_box(f'{prefix}_Sign_{cat_name}', (1.3, 0.04, 0.2), to_world(cx, -0.35, 1.52), mats['sign_dark'], c_fixt)
            ob_s.rotation_euler.z = math.radians(rot_z)
            # Text bar
            ob_t = add_box(f'{prefix}_Text_{cat_name}', (0.7, 0.01, 0.08), to_world(cx, -0.38, 1.58), mats['text_white'], c_fixt)
            ob_t.rotation_euler.z = math.radians(rot_z)
            # Floor status bar
            ob_b = add_box(f'{prefix}_Status_{cat_name}', (1.3, 0.05, 0.1), to_world(cx, -0.38, 0.1), status_mat, c_fixt)
            ob_b.rotation_euler.z = math.radians(rot_z)

        # POPULATE WITH CLEAN PRODUCTS
        # 1. Milk Cartons
        for ti, tz in enumerate(tier_z_rel):
            for i, ox in enumerate([-3.6, -3.3, -3.0]):
                wloc = to_world(ox, -0.08, tz + shelf_thk)
                # Carton
                bm = bmesh.new()
                bmesh.ops.create_cube(bm, size=1.0)
                bmesh.ops.scale(bm, vec=(0.20, 0.18, 0.32), verts=bm.verts)
                bmesh.ops.translate(bm, vec=(0, 0, 0.16), verts=bm.verts)
                # Blue cap
                bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.028, radius2=0.028, depth=0.028)
                for v in bm.verts[-24:]:
                    v.co.x += 0.03
                    v.co.y += 0.03
                    v.co.z += 0.334
                me = bpy.data.meshes.new(f'{prefix}_Milk_{ti}_{i}_Mesh')
                bm.to_mesh(me)
                bm.free()
                me.materials.append(mats['milk_body'])
                ob = bpy.data.objects.new(f'{prefix}_Milk_{ti}_{i}', me)
                ob.location = wloc
                ob.rotation_euler.z = math.radians(rot_z)
                c_prod.objects.link(ob)
                # Blue Label
                add_box(f'{prefix}_MilkLabel_{ti}_{i}', (0.12, 0.01, 0.11), to_world(ox, -0.175, tz + shelf_thk + 0.13), mats['milk_blue'], c_prod).rotation_euler.z = math.radians(rot_z)

        # 2. Rice Bags
        for ti, tz in enumerate(tier_z_rel):
            for i, ox in enumerate([-2.0, -1.7, -1.4]):
                wloc = to_world(ox, -0.08, tz + shelf_thk)
                bm = bmesh.new()
                bmesh.ops.create_cube(bm, size=1.0)
                bmesh.ops.scale(bm, vec=(0.24, 0.20, 0.22), verts=bm.verts)
                bmesh.ops.translate(bm, vec=(0, 0, 0.11), verts=bm.verts)
                me = bpy.data.meshes.new(f'{prefix}_Rice_{ti}_{i}_Mesh')
                bm.to_mesh(me)
                bm.free()
                me.materials.append(mats['rice_bag'])
                ob = bpy.data.objects.new(f'{prefix}_Rice_{ti}_{i}', me)
                ob.location = wloc
                ob.rotation_euler.z = math.radians(rot_z)
                c_prod.objects.link(ob)
                add_box(f'{prefix}_RiceLabel_{ti}_{i}', (0.15, 0.01, 0.09), to_world(ox, -0.185, tz + shelf_thk + 0.08), mats['rice_green'], c_prod).rotation_euler.z = math.radians(rot_z)

        # 3. Bread Loaves
        for ti, tz in enumerate(tier_z_rel):
            for i, ox in enumerate([-0.4, -0.1, 0.2]):
                wloc = to_world(ox, -0.08, tz + shelf_thk)
                bm = bmesh.new()
                bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=12, radius=0.11)
                bmesh.ops.scale(bm, vec=(1.0, 1.0, 0.85), verts=bm.verts)
                bmesh.ops.translate(bm, vec=(0, 0, 0.095), verts=bm.verts)
                me = bpy.data.meshes.new(f'{prefix}_Bread_{ti}_{i}_Mesh')
                bm.to_mesh(me)
                bm.free()
                me.materials.append(mats['bread_crust'])
                ob = bpy.data.objects.new(f'{prefix}_Bread_{ti}_{i}', me)
                ob.location = wloc
                ob.rotation_euler.z = math.radians(rot_z)
                c_prod.objects.link(ob)
                add_box(f'{prefix}_BreadBand_{ti}_{i}', (0.13, 0.23, 0.05), to_world(ox, -0.08, tz + shelf_thk + 0.08), mats['bread_band'], c_prod).rotation_euler.z = math.radians(rot_z)

        # 4. Egg Cartons
        for ti, tz in enumerate(tier_z_rel[:2]):
            for ei, e_off in enumerate([1.2, 1.8]):
                add_box(f'{prefix}_EggTray_{ti}_{ei}', (0.52, 0.25, 0.07), to_world(e_off, -0.08, tz + shelf_thk), mats['egg_carton'], c_prod).rotation_euler.z = math.radians(rot_z)
                for er in [-0.055, 0.055]:
                    for ec in range(6):
                        ex = e_off - 0.20 + ec * 0.08
                        bm_e = bmesh.new()
                        bmesh.ops.create_uvsphere(bm_e, u_segments=10, v_segments=8, radius=0.030)
                        bmesh.ops.scale(bm_e, vec=(1.0, 1.0, 1.25), verts=bm_e.verts)
                        bmesh.ops.translate(bm_e, vec=(0, 0, 0.08), verts=bm_e.verts)
                        me_e = bpy.data.meshes.new(f'{prefix}_Egg_{ti}_{ei}_{er}_{ec}_Mesh')
                        bm_e.to_mesh(me_e)
                        bm_e.free()
                        me_e.materials.append(mats['egg_shell'])
                        ob_e = bpy.data.objects.new(f'{prefix}_Egg_{ti}_{ei}_{er}_{ec}', me_e)
                        ob_e.location = to_world(ex, -0.08 + er, tz + shelf_thk)
                        ob_e.rotation_euler.z = math.radians(rot_z)
                        c_prod.objects.link(ob_e)

        # 5. Juice Bottles
        for ti, tz in enumerate(tier_z_rel):
            for i, ox in enumerate([2.8, 3.1, 3.4]):
                wloc = to_world(ox, -0.08, tz + shelf_thk)
                bm = bmesh.new()
                bmesh.ops.create_cone(bm, cap_ends=True, segments=14, radius1=0.075, radius2=0.075, depth=0.20)
                bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.036, radius2=0.036, depth=0.055)
                for v in bm.verts[-24:]:
                    v.co.z += 0.125
                bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.038, radius2=0.038, depth=0.03)
                for v in bm.verts[-24:]:
                    v.co.z += 0.165
                bmesh.ops.translate(bm, vec=(0, 0, 0.10), verts=bm.verts)
                me = bpy.data.meshes.new(f'{prefix}_Juice_{ti}_{i}_Mesh')
                bm.to_mesh(me)
                bm.free()
                me.materials.append(mats['juice_amber'])
                ob = bpy.data.objects.new(f'{prefix}_Juice_{ti}_{i}', me)
                ob.location = wloc
                ob.rotation_euler.z = math.radians(rot_z)
                c_prod.objects.link(ob)
                add_box(f'{prefix}_JuiceLabel_{ti}_{i}', (0.08, 0.01, 0.09), to_world(ox, -0.16, tz + shelf_thk + 0.07), mats['juice_label'], c_prod).rotation_euler.z = math.radians(rot_z)

    # Place Clean Aisle Shelves across the supermarket
    create_clean_aisle_shelf('Aisle_1_Clean', (-0.5, 0.5, 0), rot_z=-15)
    create_clean_aisle_shelf('Aisle_2_Clean', (3.5, 3.0, 0), rot_z=-15)
    create_clean_aisle_shelf('Aisle_3_Clean', (7.2, 5.5, 0), rot_z=-15)

    # Save blend file
    bpy.ops.wm.save_as_mainfile(filepath=p)
    print(f'[SUCCESS] Clean shelves successfully built into supermarket! Total objects: {len(bpy.data.objects)}')

if __name__ == '__main__':
    build_supermarket_with_clean_shelves()
