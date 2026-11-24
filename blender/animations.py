"""
Keyframe Animation Engine for Retail Waste Management Simulator.
Compatible with Blender 4.x and Blender 5.x Slotted Action System.
Implements:
1. Conveyor Belt stock arrival animation
2. Inventory shelf replenishment
3. Expiry removal & organic waste diversion
4. Surplus donation routing
5. Packaging recycling segregation
6. Hazardous waste sealed disposal
"""

import bpy
import math

def set_animation_range(start_frame=1, end_frame=250):
    """Sets scene timeline bounds."""
    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end = end_frame
    bpy.context.scene.frame_set(start_frame)

def set_action_interpolation_linear(obj):
    """Helper to set fcurves linear across both legacy Blender and Blender 5.x slotted actions."""
    anim_data = getattr(obj, "animation_data", None)
    if not anim_data or not anim_data.action:
        return
    act = anim_data.action
    # In Blender 5.0+, Action fcurves may reside under layers or channel bags or directly
    fcurves = getattr(act, "fcurves", None)
    if fcurves:
        for fcurve in fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'LINEAR'
    elif hasattr(act, "layers"):
        for layer in act.layers:
            for strip in getattr(layer, "strips", []):
                for channel_bag in getattr(strip, "channel_bags", []):
                    for fcurve in getattr(channel_bag, "fcurves", []):
                        for kf in fcurve.keyframe_points:
                            kf.interpolation = 'LINEAR'

def animate_conveyor_arrival(product_obj, start_frame=10, end_frame=70):
    """
    Animates a product traveling down the backroom conveyor belt
    from the loading dock (Y=20.0) to the staging area (Y=12.5).
    """
    product_obj.animation_data_clear()
    
    # Start position on conveyor
    product_obj.location = (0.0, 20.0, 0.95)
    product_obj.keyframe_insert(data_path="location", frame=start_frame)
    
    # End position at dispatch point
    product_obj.location = (0.0, 12.5, 0.95)
    product_obj.keyframe_insert(data_path="location", frame=end_frame)
    
    set_action_interpolation_linear(product_obj)

def animate_replenishment(product_obj, target_shelf_pos, start_frame=75, end_frame=130):
    """
    Animates a product moving from the conveyor/staging area onto the store shelf.
    Demonstrates 3D Translation, parabolic lift and rotation.
    """
    start_pos = (0.0, 12.5, 0.95)
    mid_pos = (target_shelf_pos[0] * 0.5, (start_pos[1] + target_shelf_pos[1]) * 0.5, 2.2)
    
    # Keyframe 1: Staging point
    product_obj.location = start_pos
    product_obj.keyframe_insert(data_path="location", frame=start_frame)
    
    # Keyframe 2: Lifted in transit
    product_obj.location = mid_pos
    product_obj.keyframe_insert(data_path="location", frame=(start_frame + end_frame) // 2)
    
    # Keyframe 3: Placed securely on shelf
    product_obj.location = target_shelf_pos
    product_obj.keyframe_insert(data_path="location", frame=end_frame)

def animate_waste_routing(product_obj, destination_pos, start_frame=140, end_frame=200):
    """
    Animates moving a product from its store shelf to a target waste or donation station.
    """
    start_pos = tuple(product_obj.location)
    lift_pos = (start_pos[0], start_pos[1], start_pos[2] + 0.6)
    dest_pos = tuple(destination_pos)
    
    # 1. Lift off shelf
    product_obj.keyframe_insert(data_path="location", frame=start_frame)
    product_obj.location = lift_pos
    product_obj.keyframe_insert(data_path="location", frame=start_frame + 15)
    
    # 2. Transit across store floor to Waste Station
    product_obj.location = (dest_pos[0] + 0.5, dest_pos[1], 1.8)
    product_obj.keyframe_insert(data_path="location", frame=start_frame + 45)
    
    # 3. Drop into collection container
    product_obj.location = dest_pos
    product_obj.keyframe_insert(data_path="location", frame=end_frame)
    
    # Scaling down on disposal
    product_obj.keyframe_insert(data_path="scale", frame=start_frame)
    product_obj.scale = (0.8, 0.8, 0.8)
    product_obj.keyframe_insert(data_path="scale", frame=end_frame)

def setup_demonstration_animations(product_registry, zone_metadata):
    """
    Sets up a complete automated demonstration sequence across frames 1 to 240.
    """
    set_animation_range(1, 240)
    
    # 1. Replenishment product: Pick PROD_1_01 (Apple)
    if "PROD_1_01" in product_registry:
        apple_data = product_registry["PROD_1_01"]
        apple_obj = bpy.data.objects.get(apple_data["object_name"])
        if apple_obj:
            animate_conveyor_arrival(apple_obj, start_frame=10, end_frame=55)
            animate_replenishment(apple_obj, apple_data["initial_location"], start_frame=56, end_frame=110)
            
    # 2. Expired produce product: Pick PROD_1_02 (Orange) -> Organic Waste
    if "PROD_1_02" in product_registry and "Organic" in zone_metadata:
        orange_data = product_registry["PROD_1_02"]
        orange_obj = bpy.data.objects.get(orange_data["object_name"])
        if orange_obj:
            animate_waste_routing(orange_obj, zone_metadata["Organic"]["drop_point"], start_frame=120, end_frame=180)
            
    # 3. Surplus food product: Pick PROD_1_03 (Banana) -> Donation Zone
    if "PROD_1_03" in product_registry and "Donation" in zone_metadata:
        banana_data = product_registry["PROD_1_03"]
        banana_obj = bpy.data.objects.get(banana_data["object_name"])
        if banana_obj:
            animate_waste_routing(banana_obj, zone_metadata["Donation"]["drop_point"], start_frame=130, end_frame=190)

    # 4. Hazardous chemical: Pick PROD_4_01 (Household Cleaner) -> Hazard Vault
    if "PROD_4_01" in product_registry and "Hazardous" in zone_metadata:
        chem_data = product_registry["PROD_4_01"]
        chem_obj = bpy.data.objects.get(chem_data["object_name"])
        if chem_obj:
            animate_waste_routing(chem_obj, zone_metadata["Hazardous"]["drop_point"], start_frame=140, end_frame=205)
