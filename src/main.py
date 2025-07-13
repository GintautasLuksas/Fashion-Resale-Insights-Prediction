"""
Main entry point for the Fashion Resale Insights & Prediction project.
Loads raw data, processes it, and prepares it for database insertion or modeling.
"""

from src.data_processing import load_raw_data, clean_data, engineer_features, encode_categoricals, select_final_columns
import pandas as pd

def main():
    filepath = r'C:\Users\user\PycharmProjects\Fashion-Resale-Insights-Prediction\data\raw\vestiaire.csv'

    print("🔄 Loading data...")
    df_raw = load_raw_data(filepath)

    print(f"✅ Raw data shape: {df_raw.shape}")

    print("🧼 Cleaning data...")
    df_cleaned = clean_data(df_raw)

    print("🛠️ Engineering features...")
    df_features = engineer_features(df_cleaned)

    print("🧠 Encoding categorical variables...")
    df_encoded = encode_categoricals(df_features)

    print("📦 Selecting final columns...")
    df_final = select_final_columns(df_encoded)

    print(f"📊 Final data shape: {df_final.shape}")
    print("📝 Sample rows:")
    print(df_final.head())

if __name__ == "__main__":
    main()
