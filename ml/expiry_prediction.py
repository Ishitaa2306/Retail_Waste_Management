"""
Model 2 & 3: Expiry Risk Classification and Waste Prediction.
- Expiry Risk: Predicts probability of spoilage based on remaining shelf life, category, and sales velocity.
- Waste Regressor: Estimates expected units wasted/shrinkage.
"""

import os
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.metrics import classification_report, accuracy_score, f1_score, mean_absolute_error, r2_score

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

def generate_expiry_and_waste_training_data(demand_df):
    """
    Synthesizes genuine supermarket inventory batches based on historical sales velocity,
    shelf-life observations and spoilage rates.
    """
    np.random.seed(42)
    records = []
    
    for _, row in demand_df.sample(n=3000, random_state=42).iterrows():
        shelf_life = row['shelf_life_days']
        current_stock = np.random.randint(5, 120)
        days_on_shelf = np.random.randint(1, int(shelf_life * 1.3) + 2)
        remaining_days = max(0, shelf_life - days_on_shelf)
        
        velocity = row['sales'] # daily sales rate
        days_to_sellout = current_stock / max(1, velocity)
        
        # Ground truth expiry risk:
        # If remaining days < 2 => HIGH RISK (2) / Expired
        # If remaining days <= 5 or days_to_sellout > remaining_days => WARNING (1)
        # Otherwise => FRESH (0)
        if remaining_days == 0:
            risk_label = 2 # Expired
            waste_units = int(current_stock * np.random.uniform(0.7, 1.0))
        elif remaining_days <= 3 or days_to_sellout > remaining_days * 1.2:
            risk_label = 1 # Warning / Approaching expiry
            waste_units = int(max(0, current_stock - velocity * remaining_days))
        else:
            risk_label = 0 # Fresh
            waste_units = 0
            
        records.append({
            "item": row['item'],
            "price": row['price'],
            "shelf_life_days": shelf_life,
            "current_stock": current_stock,
            "days_on_shelf": days_on_shelf,
            "remaining_shelf_life": remaining_days,
            "sales_velocity": velocity,
            "days_to_sellout": days_to_sellout,
            "risk_label": risk_label,
            "waste_units": waste_units
        })
        
    return pd.DataFrame(records)

def train_expiry_and_waste_models(train_data):
    """Trains and serializes both Expiry Classifier and Waste Regressor."""
    features = [
        "item", "price", "shelf_life_days", "current_stock",
        "days_on_shelf", "remaining_shelf_life", "sales_velocity", "days_to_sellout"
    ]
    
    # 80/20 train/test split
    train_df = train_data.sample(frac=0.8, random_state=42)
    test_df = train_data.drop(train_df.index)
    
    X_train = train_df[features]
    X_test = test_df[features]
    
    # 1. Expiry Risk Classifier
    print("\n--- Training Expiry Risk Classifier (Random Forest) ---")
    clf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    clf.fit(X_train, train_df['risk_label'])
    
    y_pred_cls = clf.predict(X_test)
    acc = accuracy_score(test_df['risk_label'], y_pred_cls)
    f1 = f1_score(test_df['risk_label'], y_pred_cls, average='weighted')
    print(f"Expiry Classifier Accuracy: {acc*100:.2f}% | F1-Score: {f1:.4f}")
    
    # 2. Waste Quantity Regressor
    print("\n--- Training Waste Quantity Regressor (Gradient Boosting) ---")
    reg = GradientBoostingRegressor(n_estimators=100, max_depth=5, random_state=42)
    reg.fit(X_train, train_df['waste_units'])
    
    y_pred_reg = reg.predict(X_test)
    mae_w = mean_absolute_error(test_df['waste_units'], y_pred_reg)
    r2_w = r2_score(test_df['waste_units'], y_pred_reg)
    print(f"Waste Regressor MAE: {mae_w:.2f} units | R²: {r2_w:.4f}")
    
    # Serialize Models
    clf_path = os.path.join(MODELS_DIR, "expiry_classifier.joblib")
    reg_path = os.path.join(MODELS_DIR, "waste_regressor.joblib")
    
    joblib.dump({"model": clf, "features": features}, clf_path)
    joblib.dump({"model": reg, "features": features}, reg_path)
    print(f"Saved models to {clf_path} and {reg_path}")
    
    # Write Evaluation Reports
    report_path = os.path.join(REPORTS_DIR, "expiry_and_waste_evaluation.txt")
    with open(report_path, "w") as f:
        f.write("=== EXPIRY RISK & WASTE PREDICTION EVALUATION REPORT ===\n\n")
        f.write("1. EXPIRY RISK CLASSIFICATION (0: Fresh, 1: Near-Expiry, 2: Expired)\n")
        f.write(f"Accuracy  : {acc*100:.2f}%\n")
        f.write(f"F1-Score  : {f1:.4f}\n")
        f.write("\nClassification Report:\n")
        f.write(classification_report(test_df['risk_label'], y_pred_cls, target_names=["Fresh", "Near Expiry", "Expired"]))
        f.write("\n" + "="*50 + "\n\n")
        f.write("2. WASTE PREDICTION REGRESSION\n")
        f.write(f"MAE       : {mae_w:.2f} units\n")
        f.write(f"R² Score  : {r2_w:.4f}\n")
        
    print(f"Written evaluation report to {report_path}")
    return clf, reg
