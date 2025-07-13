"""
Data processing functions for the Fashion Resale project.
Loads, cleans, and prepares data for database insertion and machine learning.
"""

import pandas as pd
import numpy as np


def load_raw_data(filepath):
    """
    Loads raw CSV data from the given filepath.

    Parameters:
        filepath (str): Full path to the CSV file.

    Returns:
        pd.DataFrame: Raw loaded dataset.
    """
    df = pd.read_csv(filepath, low_memory=False)
    return df


def clean_data(df):
    """
    Performs initial cleaning of the dataset.

    - Drops duplicates.
    - Removes rows with missing essential data (brand, price).
    - Casts appropriate dtypes.

    Parameters:
        df (pd.DataFrame): Raw dataset.

    Returns:
        pd.DataFrame: Cleaned dataset.
    """
    df = df.drop_duplicates()
    df = df.dropna(subset=['price_usd', 'brand_name'])

    # Convert boolean-like columns if needed
    bool_columns = ['sold', 'reserved', 'available', 'in_stock', 'should_be_gone']
    for col in bool_columns:
        df[col] = df[col].astype(bool)

    return df


def engineer_features(df):
    """
    Creates additional features for modeling and analysis.

    - Log-transforms price to reduce skew.
    - Encodes categorical variables.
    - Simplifies condition and gender labels.

    Parameters:
        df (pd.DataFrame): Cleaned dataset.

    Returns:
        pd.DataFrame: DataFrame with engineered features.
    """
    df['price_log'] = df['price_usd'].apply(lambda x: np.log1p(x) if pd.notnull(x) else np.nan)

    # Encode common categorical features
    df['brand_encoded'] = df['brand_name'].astype('category').cat.codes
    df['condition_encoded'] = df['product_condition'].astype('category').cat.codes
    df['gender_encoded'] = df['product_gender_target'].astype('category').cat.codes

    return df


def select_final_columns(df):
    """
    Filters the DataFrame to a manageable set of columns for PostgreSQL storage.

    Parameters:
        df (pd.DataFrame): Feature-engineered dataset.

    Returns:
        pd.DataFrame: Final dataset with selected features.
    """
    columns_to_keep = [
        'product_id',
        'product_type',
        'brand_name',
        'product_gender_target',
        'product_condition',
        'product_material',
        'product_color',
        'price_usd',
        'price_log',
        'sold',
        'seller_country',
        'seller_products_sold',
        'seller_pass_rate',
        'brand_encoded',
        'condition_encoded',
        'gender_encoded'
    ]
    return df[columns_to_keep]
