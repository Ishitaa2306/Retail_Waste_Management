"""
Data preprocessing, feature engineering and time-series transformation module.
Computes calendar features, lag features, rolling statistics and train-test splits.
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "datasets", "processed")

def engineer_time_features(df):
    """Generates rich calendar and cyclic features for demand forecasting."""
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_week'] = df['date'].dt.dayofweek
    df['day_of_month'] = df['date'].dt.day
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['is_weekend'] = df['day_of_week'].isin([4, 5, 6]).astype(int)
    
    # Cyclic sine/cosine encodings for month and day of week
    df['sin_month'] = np.sin(2 * np.pi * df['month'] / 12)
    df['cos_month'] = np.cos(2 * np.pi * df['month'] / 12)
    df['sin_dow'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
    df['cos_dow'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
    
    return df

def create_lag_features(df):
    """
    Computes lag sales (t-1, t-7, t-14) and 7-day rolling statistics
    grouped by item without data leakage.
    """
    df = df.sort_values(by=['item', 'date']).reset_index(drop=True)
    
    df['lag_1'] = df.groupby('item')['sales'].shift(1)
    df['lag_7'] = df.groupby('item')['sales'].shift(7)
    df['lag_14'] = df.groupby('item')['sales'].shift(14)
    
    # Rolling mean and std over past 7 days (shifted by 1 to prevent future leakage)
    df['rolling_mean_7'] = df.groupby('item')['sales'].transform(lambda x: x.shift(1).rolling(7).mean())
    df['rolling_std_7'] = df.groupby('item')['sales'].transform(lambda x: x.shift(1).rolling(7).std())
    
    # Fill initial boundary NaNs cleanly
    df = df.dropna().reset_index(drop=True)
    return df

def prepare_demand_dataset(raw_df):
    """Full preprocessing pipeline for retail demand forecasting."""
    df = raw_df.copy()
    df = engineer_time_features(df)
    df = create_lag_features(df)
    
    # Categorical one-hot encoding for category
    df = pd.get_dummies(df, columns=['category'], drop_first=False)
    
    out_path = os.path.join(PROCESSED_DIR, "preprocessed_demand.csv")
    df.to_csv(out_path, index=False)
    print(f"Saved preprocessed demand dataset with {len(df)} rows to {out_path}")
    return df

def chronological_split(df, split_date="2024-07-01"):
    """
    Splits chronological data without lookahead bias.
    Train: data before split_date
    Test: data on and after split_date
    """
    df['date'] = pd.to_datetime(df['date'])
    train_df = df[df['date'] < split_date].copy()
    test_df = df[df['date'] >= split_date].copy()
    print(f"Chronological Split: Train={len(train_df)} rows, Test={len(test_df)} rows")
    return train_df, test_df
