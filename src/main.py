from src.data_processing import load_raw_data, clean_data, engineer_features, select_final_columns

def main():
    filepath = r'C:\Users\user\PycharmProjects\Fashion-Resale-Insights-Prediction\data\raw\vestiaire.csv'

    print("🔄 Loading data...")
    df_raw = load_raw_data(filepath)
    print(f"Raw data rows: {df_raw.shape[0]}")

    print("🧼 Cleaning data...")
    df_cleaned = clean_data(df_raw)
    print(f"Rows after cleaning: {df_cleaned.shape[0]} (Dropped {df_raw.shape[0] - df_cleaned.shape[0]} rows)")

    print("🛠️ Engineering features...")
    df_features = engineer_features(df_cleaned)
    print(f"Rows after feature engineering: {df_features.shape[0]}")

    print("📦 Selecting final columns...")
    df_final = select_final_columns(df_features)
    print(f"Rows after selecting columns: {df_final.shape[0]}")

    print("📝 Sample rows:")
    print(df_final.head())

if __name__ == "__main__":
    main()
