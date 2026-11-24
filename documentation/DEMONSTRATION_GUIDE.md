# Retail Waste Management & Inventory Optimization Simulator
## College Demonstration & Presentation Guide

### 1. How to Open and View the Updated Supermarket Scene
1. **Close any running instance of Blender** (choose **Don't Save** if prompted, so memory does not overwrite the file).
2. Open Blender and load:
   `Retail_Waste_Management.blend`
3. **Switch Viewport Shading**:
   - In the top-right corner of the 3D Viewport, click the **3rd sphere (Material Preview Mode)** or the **4th sphere (Rendered Mode)** to view all PBR packaging graphics, glowing shelf LED strips, and warm spotlighting.
   - Even in **Solid Shading** (2nd sphere), all 1,764 items are assigned distinct viewport diffuse colors so shelves will never appear blank or grey.

---

### 2. Scene Contents & Visual Features
- **1,764+ Discrete 3D Products**:
  - **Fresh Produce Island Tables**: Tiered crates containing pyramids of individual 3D Red Apples, Green Apples, Citrus Oranges, Lemons, Vine Tomatoes, and Leafy Greens.
  - **Gondola Shelves (Left & Right)**: 5 tiers on each side completely filled with double-row facings of commercial beverage cans, glass jars, cereal boxes, and snack packages.
- **Lighting & Architecture**:
  - High-angle ceiling spotlight tracks with warm 3000K illumination.
  - Continuous LED light strips mounted beneath every shelf tier.
  - Category signage and porcelain floor tiling.

---

### 3. Machine Learning & Waste Simulator Defense

When explaining the system to your Computer Graphics & Machine Learning professors:

| Component | Technical Implementation | Files to Show |
| :--- | :--- | :--- |
| **Demand Forecasting** | Random Forest Regressor trained on 5-year retail daily sales ($R^2 = 0.9344$, MAE = 4.31 units). | `ml/demand_forecasting.py`, `models/demand_forecast_model.joblib` |
| **Expiry Classification** | Random Forest Classifier trained on USDA FoodKeeper storage benchmarks (99.67% accuracy). | `ml/expiry_prediction.py`, `models/expiry_classifier.joblib` |
| **Waste Mitigation** | Gradient Boosting Regressor forecasting potential kilograms wasted ($R^2 = 0.9744$). | `ml/inventory_optimization.py`, `models/waste_regressor.joblib` |
| **Simulator Integration** | Generates per-item actionable decisions (`NORMAL`, `DISCOUNT`, `DONATE`, `DISPOSE`) parsed directly into 3D state indicators. | `predictions/inventory_predictions.json` |

---

### 4. Interactive 3D Viewport & Animations
- Press `N` in the Blender 3D Viewport to open the sidebar and navigate to the **Retail Sim** panel.
- Use the built-in operators:
  - **Load ML Predictions**: Reads `predictions/inventory_predictions.json` and updates status rings above items.
  - **Trigger Restock**: Animates warehouse delivery replenishment.
  - **Trigger Donation / Waste**: Animates routing of expiring perishable items to donation and compost stations.
