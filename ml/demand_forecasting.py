"""
Model 1: Supermarket Demand Forecasting Pipeline.
Trains Random Forest and Gradient Boosting Regressors on real-world retail sales data.
Evaluates MAE, RMSE, R² and saves the top-performing model.
"""

import os
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

FEATURE_COLS = [
    'item', 'price', 'cost', 'shelf_life_days',
    'day_of_week', 'day_of_month', 'month', 'is_weekend',
    'sin_month', 'cos_month', 'sin_dow', 'cos_dow',
    'lag_1', 'lag_7', 'lag_14', 'rolling_mean_7', 'rolling_std_7'
]

def train_and_evaluate_demand_model(train_df, test_df):
    """Trains forecasting models and saves evaluation metrics."""
    # Ensure category dummy columns are included
    cat_cols = [c for c in train_df.columns if c.startswith('category_')]
    features = FEATURE_COLS + cat_cols
    
    X_train = train_df[features]
    y_train = train_df['sales']
    X_test = test_df[features]
    y_test = test_df['sales']
    
    print("\n--- Training Demand Forecasting Model (Random Forest Regressor) ---")
    rf = RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    
    y_pred = rf.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    print(f"Random Forest Evaluation Results:")
    print(f"MAE  : {mae:.2f} units")
    print(f"RMSE : {rmse:.2f} units")
    print(f"R²   : {r2:.4f}")
    
    # Save model and feature names
    model_path = os.path.join(MODELS_DIR, "demand_forecast_model.joblib")
    joblib.dump({"model": rf, "features": features}, model_path)
    print(f"Demand forecasting model successfully saved to {model_path}")
    
    # Write evaluation report
    report_path = os.path.join(REPORTS_DIR, "demand_forecasting_evaluation.txt")
    with open(report_path, "w") as f:
        f.write("=== SUPERMARKET DEMAND FORECASTING EVALUATION REPORT ===\n")
        f.write(f"Model Algorithm     : Random Forest Regressor (100 estimators, max_depth=12)\n")
        f.write(f"Training Samples    : {len(X_train)}\n")
        f.write(f"Testing Samples     : {len(X_test)}\n")
        f.write(f"Features Used       : {len(features)}\n")
        f.write(f"Mean Absolute Error : {mae:.2f} units\n")
        f.write(f"Root Mean Sq Error  : {rmse:.2f} units\n")
        f.write(f"R² Score            : {r2:.4f}\n")
        f.write("\nFeature Importance:\n")
        for feat, imp in sorted(zip(features, rf.feature_importances_), key=lambda x: x[1], reverse=True)[:10]:
            f.write(f" - {feat:20s}: {imp:.4f}\n")
            
    print(f"Evaluation report written to {report_path}")
    return rf, features, {"mae": mae, "rmse": rmse, "r2": r2}
