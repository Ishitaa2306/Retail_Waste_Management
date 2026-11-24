"""
Cameras module for Retail Waste Management Simulator.
Provides 10 designated camera perspectives covering all supermarket departments,
waste stations, CG transformation demos, and orthographic architectural views.
"""

import bpy
import math

CAMERAS_CONFIG = [
    {
        "name": "Cam_01_Supermarket_Overview",
        "location": (0.0, -22.0, 14.0),
        "rotation": (math.radians(55.0), 0.0, 0.0),
        "type": "PERSP",
        "lens": 26.0,
        "description": "Complete wide-angle supermarket view showing all aisles, checkout & zones."
    },
    {
        "name": "Cam_02_Food_Section",
        "location": (-8.5, -6.0, 4.5),
        "rotation": (math.radians(65.0), 0.0, math.radians(-30.0)),
        "type": "PERSP",
        "lens": 35.0,
        "description": "Close-up view of fresh food & perishable produce aisles."
    },
    {
        "name": "Cam_03_Electronics_Clothing",
        "location": (8.5, -6.0, 4.5),
        "rotation": (math.radians(65.0), 0.0, math.radians(30.0)),
        "type": "PERSP",
        "lens": 35.0,
        "description": "View of electronics display and apparel shelving."
    },
    {
        "name": "Cam_04_Storage_Conveyor",
        "location": (0.0, 18.0, 6.5),
        "rotation": (math.radians(70.0), 0.0, math.radians(180.0)),
        "type": "PERSP",
        "lens": 32.0,
        "description": "Backroom storage, receiving dock and animated conveyor belt."
    },
    {
        "name": "Cam_05_Waste_Donation_Zones",
        "location": (-16.0, 6.0, 5.5),
        "rotation": (math.radians(60.0), 0.0, math.radians(-65.0)),
        "type": "PERSP",
        "lens": 30.0,
        "description": "Detailed view of Donation, Recycling, Organic and Hazardous Waste stations."
    },
    {
        "name": "Cam_06_Isometric_TopView",
        "location": (22.0, -22.0, 28.0),
        "rotation": (math.radians(54.736), 0.0, math.radians(45.0)),
        "type": "ORTHO",
        "ortho_scale": 42.0,
        "description": "True orthographic architectural axonometric / isometric store plan."
    },
    {
        "name": "Cam_07_Expiry_Demonstration",
        "location": (-4.5, 0.0, 3.2),
        "rotation": (math.radians(75.0), 0.0, math.radians(-45.0)),
        "type": "PERSP",
        "lens": 50.0,
        "description": "Focus camera for Color-coded Expiry detection (Green/Yellow/Red)."
    },
    {
        "name": "Cam_08_Replenishment_Demonstration",
        "location": (2.0, 8.0, 4.0),
        "rotation": (math.radians(68.0), 0.0, math.radians(140.0)),
        "type": "PERSP",
        "lens": 45.0,
        "description": "Dynamic camera tracking restock movement from storage to shelf."
    },
    {
        "name": "Cam_09_Checkout_Area",
        "location": (0.0, -11.0, 4.5),
        "rotation": (math.radians(65.0), 0.0, math.radians(180.0)),
        "type": "PERSP",
        "lens": 35.0,
        "description": "Front-of-store POS checkout counters and cart staging."
    },
    {
        "name": "Cam_10_Hazardous_Waste_Vault",
        "location": (-12.0, -7.0, 3.2),
        "rotation": (math.radians(65.0), 0.0, math.radians(-75.0)),
        "type": "PERSP",
        "lens": 42.0,
        "description": "Dedicated view of sealed Hazardous Chemical & Battery disposal."
    }
]

def setup_cameras(collection):
    created_cameras = {}
    for cfg in CAMERAS_CONFIG:
        cam_data = bpy.data.cameras.new(name=cfg["name"] + "_Data")
        cam_data.type = cfg["type"]
        if cfg["type"] == "PERSP":
            cam_data.lens = cfg["lens"]
            cam_data.clip_start = 0.1
            cam_data.clip_end = 250.0
        else:
            cam_data.ortho_scale = cfg["ortho_scale"]
            cam_data.clip_start = 0.1
            cam_data.clip_end = 250.0
            
        cam_obj = bpy.data.objects.new(name=cfg["name"], object_data=cam_data)
        cam_obj.location = cfg["location"]
        cam_obj.rotation_euler = cfg["rotation"]
        
        collection.objects.link(cam_obj)
        created_cameras[cfg["name"]] = cam_obj
        
    if "Cam_01_Supermarket_Overview" in created_cameras:
        bpy.context.scene.camera = created_cameras["Cam_01_Supermarket_Overview"]
        
    return created_cameras
