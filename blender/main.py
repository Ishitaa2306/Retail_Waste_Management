"""
Main Execution Script for Blender 3D Supermarket Simulator.
Can be executed from Blender Scripting Workspace or headless CLI:
blender --background --python blender/main.py
"""

import bpy
import os
import sys

# Add blender directory to sys.path
blend_dir = os.path.dirname(os.path.abspath(__file__))
if blend_dir not in sys.path:
    sys.path.insert(0, blend_dir)

import scene_builder

def main():
    print("=" * 60)
    print("3D RETAIL WASTE MANAGEMENT & INVENTORY OPTIMIZATION SIMULATOR")
    print("Building Supermarket Foundation (Phase 1)...")
    print("=" * 60)
    
    metadata = scene_builder.build_complete_scene()
    
    # Save blend file in root workspace
    workspace_root = os.path.dirname(blend_dir)
    output_blend = os.path.join(workspace_root, "Retail_Waste_Management.blend")
    
    bpy.ops.wm.save_as_mainfile(filepath=output_blend)
    print(f"\n[SUCCESS] Project file successfully saved to:\n{output_blend}")
    print("=" * 60)

if __name__ == "__main__":
    main()
