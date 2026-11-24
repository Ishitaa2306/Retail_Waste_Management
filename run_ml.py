"""
Master pipeline execution script.
Executes dataset ingestion, preprocessing, training, evaluation and decision generation.
"""

import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from ml import data_loader
from ml import data_preprocessing
from ml import demand_forecasting
from ml import expiry_prediction
from ml import inventory_optimization

def run_pipeline():
    print("=" * 60)
    print("STEP 1: INGESTING REAL BENCHMARK DATASETS...")
    print("=" * 60)
    demand_df = data_loader.load_or_fetch_demand_data()
    waste_df = data_loader.load_or_fetch_shelf_life_and_waste_data()
    
    print("\n" + "=" * 60)
    print("STEP 2: PREPROCESSING AND FEATURE ENGINEERING...")
    print("=" * 60)
    processed_df = data_preprocessing.prepare_demand_dataset(demand_df)
    train_df, test_df = data_preprocessing.chronological_split(processed_df, split_date="2024-07-01")
    
    print("\n" + "=" * 60)
    print("STEP 3: TRAINING & EVALUATING DEMAND FORECASTING MODEL...")
    print("=" * 60)
    rf_model, features, metrics = demand_forecasting.train_and_evaluate_demand_model(train_df, test_df)
    
    print("\n" + "=" * 60)
    print("STEP 4: TRAINING & EVALUATING EXPIRY & WASTE PREDICTION MODELS...")
    print("=" * 60)
    expiry_data = expiry_prediction.generate_expiry_and_waste_training_data(demand_df)
    clf, reg = expiry_prediction.train_expiry_and_waste_models(expiry_data)
    
    print("\n" + "=" * 60)
    print("STEP 5: EXECUTING INVENTORY OPTIMIZATION DECISION ENGINE...")
    print("=" * 60)
    decisions = inventory_optimization.generate_inventory_decisions()
    
    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE: ALL MODELS TRAINED AND PREDICTIONS EXPORTED!")
    print("=" * 60)

if __name__ == "__main__":
    run_pipeline()
