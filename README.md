# 3D Retail Waste Management & Inventory Optimization Simulator

An academic Computer Graphics and Machine Learning project combining **Blender 3D procedural modeling & animation** with **real-world retail predictive analytics**.

---

## 🏬 Project Architecture Overview

```
Retail_Waste_Management_Simulator/
│
├── blender/                        # 3D Supermarket Modeling & Animation Modules
│   ├── main.py                     # Master execution & .blend generator
│   ├── scene_builder.py            # Scene assembly orchestrator
│   ├── supermarket.py              # Architecture, 6 aisles, checkout & 4 waste zones
│   ├── products.py                 # 3D procedural product models (Food, Tech, Apparel, Hazard)
│   ├── materials.py                # PBR Principled BSDF & Checker floor materials
│   ├── cameras.py                  # 8 Academic camera viewpoints (Persp & Ortho)
│   ├── animations.py               # Keyframe conveyor, replenishment & waste routing
│   └── controls.py                 # Interactive 3D Viewport UI Panel
│
├── ml/                             # Machine Learning Pipeline
│   ├── data_loader.py              # Real-world retail dataset ingestion
│   ├── data_preprocessing.py       # Time-series feature engineering & lag creation
│   ├── demand_forecasting.py       # Demand prediction models (Random Forest / XGBoost)
│   ├── expiry_prediction.py        # Shelf-life risk categorization
│   ├── waste_prediction.py         # Expected waste & shrinkage estimation
│   ├── inventory_optimization.py   # Decision engine (Restock, Donate, Recycle, Hazard Disposal)
│   └── prediction_service.py       # JSON prediction exporter for Blender
│
├── datasets/
│   ├── raw/                        # Original benchmark datasets
│   └── processed/                  # Preprocessed training sets
│
├── models/                         # Serialized ML models (.joblib)
├── predictions/                    # JSON data bridge connecting ML to Blender
├── renders/                        # Rendered demonstration snapshots
└── Retail_Waste_Management.blend   # Saved master Blender scene
```

---

## 🚀 How to Open and Run in Blender

1. **Launch Blender 5.3 (or 4.x+)**.
2. Go to **File -> Open** and select:
   ```
   C:\Users\Ishita\Retail_Waste_Management_Simulator\Retail_Waste_Management.blend
   ```
3. Switch 3D Viewport shading to **Material Preview** or **Rendered** mode (top-right sphere icons in the 3D viewport) to see all PBR colors, lights and textures.
4. Press **Spacebar** on your keyboard to play the animation timeline (Frames 1–240) and watch:
   - Conveyor belt stock arrival.
   - Restocking onto shelves.
   - Perishable organic waste removal.
   - Surplus food donation transfer.
   - Hazardous chemical isolation.
5. In the 3D Viewport, press **N** to expand the sidebar and click on the **Retail Simulator** tab to:
   - Switch camera perspectives instantly (Isometric Top-view, Food Aisles, Storage, Waste Stations).
   - Refresh ML predictions and trigger actions.
