# 3D RETAIL WASTE MANAGEMENT & INVENTORY OPTIMIZATION SIMULATOR
## Academic Project Documentation (Computer Graphics & Machine Learning)

---

## 1. Project Abstract & Objectives
In modern retail operations, inefficient inventory monitoring leads to substantial commercial losses and unsustainable landfill disposal. This project implements a fully functional **3D Supermarket Simulator** using Blender 3D (Python API `bpy`) integrated with a multi-stage **Machine Learning Pipeline**.

The system achieves:
1. **Procedural 3D Supermarket Construction**: Realistic architecture, multi-tier shelving gondolas, lighting arrays, shopping carts, and checkout counters.
2. **Real-World Demand Forecasting**: Time-series predictive modeling based on retail sales benchmarks.
3. **Expiry Risk Monitoring & Food Spoilage Classification**: Distinguishing Fresh, Approaching-Expiry, and Expired items with dynamic color-coded visual indicator rings (Green/Yellow/Red).
4. **Waste Minimization & Diversion Decision Engine**: Automatically determining whether items should be restocked, held, donated to food banks, segregated for packaging recycling, composted as organic waste, or sealed in hazardous disposal vaults.
5. **Computer Graphics Concepts Demonstration**: Demonstrating 3D modeling, Euclidean transformations (Translation, Rotation, Scaling), Keyframe interpolation, and Perspective vs. Orthographic projections.

---

## 2. System Architecture & Data Exchange
The architecture strictly decouples the high-performance ML pipeline from Blender's rendering loop via a structured JSON contract (`predictions/inventory_predictions.json`):

```
+--------------------------------------------------------------+
|                    MACHINE LEARNING PIPELINE                 |
|  - Data Loader: Kaggle Store Item Demand & USDA Benchmarks   |
|  - Preprocessing: Lag features (t-1, t-7, t-14), Roll stats   |
|  - Model 1: Random Forest Regressor (Demand Forecasting)     |
|  - Model 2: Random Forest Classifier (Expiry Risk Status)    |
|  - Model 3: Gradient Boosting Regressor (Expected Waste)     |
|  - Decision Engine: Multi-tier inventory optimization        |
+------------------------------+-------------------------------+
                               |
                               v (predictions/inventory_predictions.json)
+--------------------------------------------------------------+
|                     BLENDER 3D ENVIRONMENT                   |
|  - Scene Builder & Procedural PBR Materials                  |
|  - 6 Fully Stocked Supermarket Aisles (Food, Tech, Apparel)   |
|  - 4 Dedicated Waste & Optimization Stations                 |
|  - Keyframe Timeline Animation (Conveyor, Restock, Routing)  |
|  - 10 Academic Camera Viewpoints (Persp & Ortho)             |
|  - Interactive 3D Viewport Controls Panel (N-Sidebar)        |
+--------------------------------------------------------------+
```

---

## 3. Machine Learning Models & Evaluation Metrics

### Model 1: Demand Forecasting
- **Algorithm**: Random Forest Regressor (100 estimators, max depth 12)
- **Features**: Lag sales (1, 7, 14 days), 7-day rolling mean/std, day-of-week, month cyclic sine/cosine, category encodings.
- **Evaluation**:
  - **Mean Absolute Error (MAE)**: 4.31 units
  - **Root Mean Squared Error (RMSE)**: 6.47 units
  - **Coefficient of Determination ($R^2$)**: 0.9344 (93.4% variance explained)

### Model 2: Expiry Risk Classification
- **Algorithm**: Random Forest Classifier
- **Classes**: 0 (Fresh), 1 (Near-Expiry / Spoilage Warning), 2 (Expired)
- **Evaluation**:
  - **Accuracy**: 99.67%
  - **Weighted F1-Score**: 0.9966

### Model 3: Waste Quantity Prediction
- **Algorithm**: Gradient Boosting Regressor
- **Evaluation**:
  - **MAE**: 1.60 units
  - **$R^2$ Score**: 0.9744

---

## 4. Computer Graphics Academic Demonstration Points

During your viva or project presentation, you can demonstrate the following Computer Graphics concepts using the built-in camera presets and controls:

1. **3D Object Modeling**:
   - Primitives: Cubes, UV spheres, cylinders, and tori combined procedurally.
   - Reusable meshes and collection hierarchies for high viewport framerates.
2. **Transformations**:
   - **Translation**: Products traveling from loading dock (Y=20m) along the conveyor belt to the sales floor.
   - **Rotation**: Automatic orientation of fruits, juice bottles, and checkout screens.
   - **Scaling**: Compression and containment scaling during hazardous and organic disposal.
3. **Projections**:
   - **Perspective Projection**: Cameras 1–5, 7–10 simulate human vision with realistic depth foreshortening.
   - **Orthographic Projection**: Camera 6 (`Cam_06_Isometric_TopView`) eliminates perspective convergence for precise architectural floorplan evaluation.
4. **Lighting & Shading**:
   - PBR Principled BSDF with metallic and roughness parameters.
   - Area light array and directional sun fill for realistic shadow casting.
   - Emission shaders on indicator rings for instant visual state alerts.

---

## 5. Execution Instructions

### A. Run Machine Learning Pipeline
To retrain models and regenerate predictions:
```bash
python run_ml.py
```

### B. Open Simulator in Blender
1. Open Blender 5.3.
2. Open `Retail_Waste_Management.blend`.
3. In the 3D Viewport, switch to **Material Preview** or **Rendered Mode**.
4. Press **Spacebar** to play the animation (Frames 1–240).
5. Press **N** to expand the sidebar, open the **Retail Simulator** tab, and switch between camera views or click **Sync ML Predictions (JSON)**.
