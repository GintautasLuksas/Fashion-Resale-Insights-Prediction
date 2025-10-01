"""
Main script to run data loading, cleaning, and processing pipeline.
"""

from src.data_processing import (
    load_raw_data,
    clean_data,
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

        print("Loading data")
        df_raw = load_raw_data(filepath)
        print(f"Raw data rows: {df_raw.shape[0]}")

        print("Data cleaning in progress")
        df_cleaned = clean_data(df_raw)
        print(f"Rows after cleaning: {df_cleaned.shape[0]} (Dropped {df_raw.shape[0] - df_cleaned.shape[0]} rows)")


        print("📦Selecting final columns for DB")
        df_final = select_final_columns(df_cleaned)
        print(f"Final dataset shape: {df_final.shape}")

        print("Sample rows:")
        print(df_final.head())

        '''Processed csv saved for debugging purposes'''
        processed_csv_path = r'C:\Users\user\PycharmProjects\Fashion-Resale-Insights-Prediction\data\processed\vestiaire_processed.csv'
        df_final.to_csv(processed_csv_path, index=False)
        print(f"Processed data saved to CSV: {processed_csv_path}")

        print("Inserting data to PostgreSQL")
        insert_dataframe_to_postgres(df_final, table_name="fashion_resale")
        print("Data inserted")

    except Exception as e:
        print(f"Error in the process: {e}")

if __name__ == "__main__":
    main()
