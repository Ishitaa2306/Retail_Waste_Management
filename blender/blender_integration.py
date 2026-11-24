"""
Blender ML Integration Module.
Reads predictions/inventory_predictions.json and dynamically updates 3D scene objects:
- Replaces material on indicator rings (Green/Yellow/Red)
- Triggers replenishment and waste routing actions
"""

import bpy
import json
import os

def load_predictions_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pred_path = os.path.join(base_dir, "predictions", "inventory_predictions.json")
    if not os.path.exists(pred_path):
        return None
    with open(pred_path, "r") as f:
        return json.load(f)

def apply_predictions_to_scene():
    data = load_predictions_data()
    if not data:
        return False, "Prediction JSON not found"
        
    count = 0
    for item in data:
        sku = item.get("sku")
        risk_color = item.get("risk_status", "GREEN").capitalize()
        mat_name = f"Mat_Status_{risk_color}"
        
        target_mat = bpy.data.materials.get(mat_name)
        if not target_mat:
            continue
            
        indicator_name = f"{sku}_IndicatorRing"
        indicator_obj = bpy.data.objects.get(indicator_name)
        if indicator_obj:
            indicator_obj.data.materials.clear()
            indicator_obj.data.materials.append(target_mat)
            count += 1
            
    return True, f"Updated {count} products in 3D scene with latest ML status!"
