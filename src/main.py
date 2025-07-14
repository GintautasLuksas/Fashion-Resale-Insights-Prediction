"""
Main script to run data loading, cleaning, and processing pipeline.
"""

from src.data_processing import (
    load_raw_data,
    clean_data,
    engineer_features,
    select_final_columns
)
from src.db.insert import insert_dataframe_to_postgres

def main():
    """
    Runs the full data processing pipeline:
    loads raw CSV, cleans data, engineers features, selects columns,
    optionally saves to CSV, and inserts into PostgreSQL.
    """
    try:
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
        print(f"Final dataset shape: {df_final.shape}")

        print("📝 Sample rows:")
        print(df_final.head())

        # Optional: Save processed data to CSV for backup/debug
        processed_csv_path = r'C:\Users\user\PycharmProjects\Fashion-Resale-Insights-Prediction\data\processed\vestiaire_processed.csv'
        df_final.to_csv(processed_csv_path, index=False)
        print(f"✅ Processed data saved to CSV: {processed_csv_path}")

        print("🚀 Inserting data into PostgreSQL...")
        insert_dataframe_to_postgres(df_final, table_name="fashion_resale")
        print("✅ Data inserted successfully!")

    except Exception as e:
        print(f"❌ Error during processing: {e}")

if __name__ == "__main__":
    main()
