"""
Scene Builder module for Retail Waste Management Simulator.
Coordinates initialization, geometry creation, materials, cameras, lighting and registration.
"""

import bpy
import os
import sys

# Ensure current script folder is on path for module resolution
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import materials
import cameras
import supermarket
import products
import animations
import controls

def clear_existing_scene():
    """Wipes default objects from Blender scene to guarantee a clean slate."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    for block in [bpy.data.meshes, bpy.data.materials, bpy.data.lights, bpy.data.cameras]:
        for item in block:
            block.remove(item)

def configure_render_settings():
    """Configures modern render engine (Eevee Next / Cycles fallback) with ambient occlusion."""
    scene = bpy.context.scene
    # Support modern Blender 4.x and 5.x Eevee
    scene.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items else 'BLENDER_EEVEE'
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100

def build_complete_scene():
    """Main constructor building the entire 3D supermarket environment."""
    print("[SceneBuilder] Initializing Clean Scene...")
    clear_existing_scene()
    configure_render_settings()
    
    # Root Collection
    root_col = bpy.data.collections.new("Retail_Simulator_Master")
    bpy.context.scene.collection.children.link(root_col)
    
    print("[SceneBuilder] Building Materials...")
    mat_dict = materials.init_all_materials()
    
    print("[SceneBuilder] Setting up 8 Multi-Angle Cameras...")
    cam_dict = cameras.setup_cameras(root_col)
    
    print("[SceneBuilder] Constructing Supermarket Architecture & Lighting...")
    arch_col = supermarket.build_architecture(mat_dict, root_col)
    
    print("[SceneBuilder] Assembling 6 Supermarket Aisles & Shelves...")
    aisle_col, aisle_meta = supermarket.build_aisles(mat_dict, root_col)
    
    print("[SceneBuilder] Installing Checkout Counters & Registers...")
    chk_col = supermarket.build_checkout_area(mat_dict, root_col)
    
    print("[SceneBuilder] Constructing Backroom Storage & Restock Conveyor...")
    storage_col = supermarket.build_storage_and_conveyor(mat_dict, root_col)
    
    print("[SceneBuilder] Establishing 4 Dedicated Waste Management & Donation Stations...")
    waste_col, zone_meta = supermarket.build_waste_management_zones(mat_dict, root_col)
    
    print("[SceneBuilder] Populating Shelves with 3D Products across 4 Categories...")
    prod_col, prod_registry = products.populate_supermarket_shelves(aisle_meta, root_col)
    
    print("[SceneBuilder] Generating Keyframe Animation Sequences...")
    animations.setup_demonstration_animations(prod_registry, zone_meta)
    
    print("[SceneBuilder] Registering Interactive Viewport UI Controls...")
    controls.register_controls()
    
    print("[SceneBuilder] Supermarket Environment Construction Complete!")
    return {
        "cameras": cam_dict,
        "aisles": aisle_meta,
        "zones": zone_meta,
        "products": prod_registry
    }

if __name__ == "__main__":
    build_complete_scene()
