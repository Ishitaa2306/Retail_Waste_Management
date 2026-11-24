"""
Interactive 3D Viewport Controls Panel and Operators for Blender.
Provides UI buttons for all 10 cameras, ML prediction loading, and waste actions.
"""

import bpy
import json
import os

class RETAIL_OT_LoadMLPredictions(bpy.types.Operator):
    bl_idname = "retail.load_ml_predictions"
    bl_label = "Load ML Predictions"
    bl_description = "Reads predictions JSON and updates visual status indicators in 3D"

    def execute(self, context):
        try:
            import blender_integration
            success, msg = blender_integration.apply_predictions_to_scene()
            if success:
                self.report({'INFO'}, msg)
                return {'FINISHED'}
            else:
                self.report({'WARNING'}, msg)
                return {'CANCELLED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to apply predictions: {e}")
            return {'CANCELLED'}

class RETAIL_OT_SwitchCamera(bpy.types.Operator):
    bl_idname = "retail.switch_camera"
    bl_label = "Switch View"
    camera_name: bpy.props.StringProperty()

    def execute(self, context):
        cam = bpy.data.objects.get(self.camera_name)
        if cam:
            context.scene.camera = cam
            self.report({'INFO'}, f"Active camera: {self.camera_name}")
            return {'FINISHED'}
        self.report({'WARNING'}, f"Camera {self.camera_name} not found")
        return {'CANCELLED'}

class RETAIL_OT_PlayAnimation(bpy.types.Operator):
    bl_idname = "retail.play_simulation"
    bl_label = "Start Simulation"

    def execute(self, context):
        bpy.ops.screen.animation_cancel(restore_frame=False)
        context.scene.frame_set(1)
        bpy.ops.screen.animation_play()
        self.report({'INFO'}, "Simulation timeline playing (Frames 1-240)...")
        return {'FINISHED'}

class RETAIL_OT_ResetSimulation(bpy.types.Operator):
    bl_idname = "retail.reset_simulation"
    bl_label = "Reset Simulation"

    def execute(self, context):
        bpy.ops.screen.animation_cancel(restore_frame=False)
        context.scene.frame_set(1)
        self.report({'INFO'}, "Simulation reset to frame 1.")
        return {'FINISHED'}

class RETAIL_PT_SimulatorPanel(bpy.types.Panel):
    bl_label = "Retail Waste & Inventory AI"
    bl_idname = "RETAIL_PT_simulator_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Retail Simulator'

    def draw(self, context):
        layout = self.layout

        # Section 1: Machine Learning Status
        box_ml = layout.box()
        box_ml.label(text="Machine Learning Engine", icon='SCRIPTPLUG')
        box_ml.operator("retail.load_ml_predictions", text="Sync ML Predictions (JSON)", icon='FILE_REFRESH')
        
        # Section 2: Simulation Controls
        box_sim = layout.box()
        box_sim.label(text="Simulation Timeline", icon='PLAY')
        row = box_sim.row(align=True)
        row.operator("retail.play_simulation", text="Play", icon='PLAY')
        row.operator("screen.animation_cancel", text="Pause", icon='PAUSE')
        row.operator("retail.reset_simulation", text="Reset", icon='REW')

        # Section 3: Camera Perspectives (CG Concepts)
        box_cam = layout.box()
        box_cam.label(text="Camera Views & CG Concepts", icon='CAMERA_DATA')
        
        cams = [
            ("Cam_01_Supermarket_Overview", "1. Supermarket Overview"),
            ("Cam_02_Food_Section", "2. Food & Fresh Produce"),
            ("Cam_03_Electronics_Clothing", "3. Electronics & Apparel"),
            ("Cam_04_Storage_Conveyor", "4. Storage & Restock Belt"),
            ("Cam_05_Waste_Donation_Zones", "5. 4 Waste & Donation Zones"),
            ("Cam_06_Isometric_TopView", "6. Isometric (Orthographic)"),
            ("Cam_07_Expiry_Demonstration", "7. Expiry Monitoring (HUD)"),
            ("Cam_08_Replenishment_Demonstration", "8. Restock Trajectory"),
            ("Cam_09_Checkout_Area", "9. Checkout & Shopping Carts"),
            ("Cam_10_Hazardous_Waste_Vault", "10. Hazardous Waste Vault")
        ]
        
        for c_id, label in cams:
            op = box_cam.operator("retail.switch_camera", text=label)
            op.camera_name = c_id

classes = (
    RETAIL_OT_LoadMLPredictions,
    RETAIL_OT_SwitchCamera,
    RETAIL_OT_PlayAnimation,
    RETAIL_OT_ResetSimulation,
    RETAIL_PT_SimulatorPanel,
)

def register_controls():
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            pass

def unregister_controls():
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except ValueError:
            pass
