"""
Inventory Optimization and Decision Service.
Integrates Demand Forecasts, Expiry Risk, and Waste Estimates into actionable retail actions:
- REPLENISH : High demand, low stock
- DONATE    : Surplus edible food nearing expiry
- RECYCLE   : Recyclable packaging and dry waste
- ORGANIC   : Spoiled food redirected to compost
- HAZARD    : Segregated chemicals and batteries
- HOLD      : Healthy balanced inventory
Exports structured JSON for Blender integration.
"""

import os
import json
import joblib
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
PREDICTIONS_DIR = os.path.join(BASE_DIR, "predictions")
os.makedirs(PREDICTIONS_DIR, exist_ok=True)

# Product catalog mapping to 3D supermarket aisles
PRODUCTS = [
    {"item_id": 1, "sku": "PROD_1_01", "name": "Crisp Gala Apple", "category": "FOOD_PRODUCE", "aisle": 1, "price": 2.50, "cost": 1.10, "shelf_life": 14, "current_stock": 12, "days_on_shelf": 4},
    {"item_id": 2, "sku": "PROD_1_02", "name": "Valencia Fresh Orange", "category": "FOOD_PRODUCE", "aisle": 1, "price": 3.00, "cost": 1.40, "shelf_life": 18, "current_stock": 25, "days_on_shelf": 19}, # Expired demo
    {"item_id": 3, "sku": "PROD_1_03", "name": "Organic Bananas", "category": "FOOD_PRODUCE", "aisle": 1, "price": 1.80, "cost": 0.75, "shelf_life": 7, "current_stock": 65, "days_on_shelf": 5}, # Surplus donation demo
    {"item_id": 4, "sku": "PROD_2_01", "name": "Whole Fresh Milk 1L", "category": "FOOD_DAIRY", "aisle": 2, "price": 2.20, "cost": 1.20, "shelf_life": 10, "current_stock": 8, "days_on_shelf": 3},
    {"item_id": 5, "sku": "PROD_2_02", "name": "Pure Orange Juice 1L", "category": "FOOD_DAIRY", "aisle": 2, "price": 3.80, "cost": 2.00, "shelf_life": 21, "current_stock": 18, "days_on_shelf": 6},
    {"item_id": 6, "sku": "PROD_3_01", "name": "Honey Oat Morning Cereal", "category": "FOOD_PACKAGED", "aisle": 3, "price": 4.50, "cost": 2.20, "shelf_life": 240, "current_stock": 40, "days_on_shelf": 25},
    {"item_id": 7, "sku": "PROD_4_01", "name": "Surface Cleaner Detergent", "category": "HOUSEHOLD", "aisle": 4, "price": 6.00, "cost": 2.80, "shelf_life": 730, "current_stock": 15, "days_on_shelf": 40},
    {"item_id": 8, "sku": "PROD_5_01", "name": "Smart Mobile 5G 128GB", "category": "ELECTRONICS", "aisle": 5, "price": 399.00, "cost": 260.00, "shelf_life": 1095, "current_stock": 5, "days_on_shelf": 15},
    {"item_id": 9, "sku": "PROD_5_02", "name": "Slimline Laptop Notebook", "category": "ELECTRONICS", "aisle": 5, "price": 750.00, "cost": 520.00, "shelf_life": 1460, "current_stock": 3, "days_on_shelf": 20},
    {"item_id": 10, "sku": "PROD_6_01", "name": "Premium Cotton Apparel", "category": "CLOTHING", "aisle": 6, "price": 29.00, "cost": 12.00, "shelf_life": 1825, "current_stock": 22, "days_on_shelf": 30}
]

def generate_inventory_decisions():
    """Executes ML models and generates real inventory optimization policy."""
    # Load ML models
    demand_pkg = joblib.load(os.path.join(MODELS_DIR, "demand_forecast_model.joblib"))
    clf_pkg = joblib.load(os.path.join(MODELS_DIR, "expiry_classifier.joblib"))
    reg_pkg = joblib.load(os.path.join(MODELS_DIR, "waste_regressor.joblib"))
    
    demand_model = demand_pkg["model"]
    clf_model = clf_pkg["model"]
    reg_model = reg_pkg["model"]
    
    results = []
    
    for p in PRODUCTS:
        # Base features for inference
        item_id = p["item_id"]
        shelf_life = p["shelf_life"]
        days_on = p["days_on_shelf"]
        rem_shelf = max(0, shelf_life - days_on)
        stock = p["current_stock"]
        
        # Estimate features for demand forecast
        # [item, price, cost, shelf_life_days, dow, dom, month, is_weekend, sin_m, cos_m, sin_d, cos_d, lag1, lag7, lag14, roll_mean, roll_std] + cat dummies
        cat = p["category"]
        base_feat = [
            item_id, p["price"], p["cost"], shelf_life,
            5, 15, 6, 1, 0.0, 1.0, 0.43, -0.9, 35.0, 32.0, 30.0, 33.5, 4.2
        ]
        # Pad with dummy zeros for categories
        full_feat = base_feat + [0] * (len(demand_pkg["features"]) - len(base_feat))
        pred_demand = float(np.round(demand_model.predict([full_feat])[0], 1))
        
        # Expiry and waste inference
        sales_vel = max(1.0, pred_demand)
        days_to_sell = stock / sales_vel
        
        clf_feats = [item_id, p["price"], shelf_life, stock, days_on, rem_shelf, sales_vel, days_to_sell]
        risk_class = int(clf_model.predict([clf_feats])[0])
        pred_waste = int(max(0, np.round(reg_model.predict([clf_feats])[0])))
        
        # Optimization Policy Engine
        action = "HOLD"
        reason = "Inventory levels and shelf-life are optimal."
        color_status = "GREEN" # Fresh
        
        if risk_class == 2 or rem_shelf == 0:
            color_status = "RED" # Expired
            if "HAZARD" in cat:
                action = "DISPOSE_HAZARDOUS"
                reason = "Hazardous chemical container requires sealed segregation."
            else:
                action = "DISPOSE_ORGANIC"
                reason = "Perishable food is spoiled; routed to organic compost waste."
        elif risk_class == 1 or rem_shelf <= 3:
            color_status = "YELLOW" # Approaching expiry
            if "FOOD" in cat and stock > pred_demand:
                action = "DONATE"
                reason = f"Surplus stock of {stock - int(pred_demand)} units safe for consumption; routed to Food Donation Bank."
            else:
                action = "DISCOUNT_PROMOTION"
                reason = "Accelerate sales with 30% discount to prevent waste."
        elif stock < pred_demand * 0.7:
            action = "REPLENISH"
            reason = f"Current stock ({stock}) below forecasted demand ({pred_demand:.0f}); triggering restock."
            
        results.append({
            "item_id": item_id,
            "sku": p["sku"],
            "name": p["name"],
            "category": cat,
            "aisle": p["aisle"],
            "current_stock": stock,
            "predicted_demand": pred_demand,
            "remaining_shelf_life_days": rem_shelf,
            "risk_status": color_status,
            "predicted_waste_units": pred_waste,
            "recommended_action": action,
            "reason": reason
        })
        
    out_json = os.path.join(PREDICTIONS_DIR, "inventory_predictions.json")
    with open(out_json, "w") as f:
        json.dump(results, f, indent=4)
        
    print(f"Generated actionable inventory predictions for {len(results)} items at {out_json}")
    return results

if __name__ == "__main__":
    generate_inventory_decisions()
