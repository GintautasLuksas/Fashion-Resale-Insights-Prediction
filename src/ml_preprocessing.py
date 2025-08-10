"""
ML preprocessing pipeline for Fashion Resale dataset.
Includes advanced cleaning, feature engineering, encoding, and scaling.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder


def advanced_impute_and_clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Advanced missing value imputation and normalization for ML use.

    - Fill missing text columns with placeholder.
    - Normalize text columns (lowercase, strip).
    - Fill missing numeric seller stats with 0.
    - Convert booleans consistently.
    - Drop or flag rows missing essential info if needed.
    """
    # Fill missing text fields
    text_cols = ['product_name', 'product_description', 'product_keywords']
    for col in text_cols:
        df[col] = df[col].fillna('no info')

    # Normalize text categorical columns
    cat_text_cols = [
        'product_type', 'product_category', 'product_season',
        'product_gender_target', 'product_condition',
        'product_material', 'product_color',
        'seller_badge', 'warehouse_name', 'seller_country'
    ]
    for col in cat_text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.lower().str.strip()

    # Fill missing numeric seller stats with 0 or median
    seller_num_cols = [
        'seller_products_sold', 'seller_num_products_listed',
        'seller_num_followers', 'seller_pass_rate',
        'product_like_count', 'price_usd', 'seller_price', 'seller_earning'
    ]
    for col in seller_num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)

    # Convert boolean columns explicitly
    bool_cols = ['sold', 'reserved', 'available', 'in_stock', 'should_be_gone', 'has_cross_border_fees', 'buyers_fees']
    for col in bool_cols:
        if col in df.columns:
            df[col] = (
                df[col].astype(str)
                .str.lower()
                .map({'true': True, 'false': False, '1': True, '0': False})
                .fillna(False)
                .astype('boolean')
            )

    # TODO: Consider dropping rows missing critical info (product_id, brand_name)
    df = df.dropna(subset=['product_id', 'brand_name'])

    return df


def text_processing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Simple text cleaning for product_name, description, keywords.
    Removes special characters and lowercases.
    """
    for col in ['product_name', 'product_description', 'product_keywords']:
        if col in df.columns:
            df[col] = (
                df[col]
                .str.lower()
                .str.replace(r'[^\w\s]', '', regex=True)
                .str.strip()
            )
    return df


def encode_categoricals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Encode categorical columns with label encoding or one-hot encoding.

    - Use label encoding for high cardinality columns.
    - Use one-hot for low cardinality columns.
    """

    # Label encoding for brand_name, seller_id (high cardinality)
    label_encode_cols = ['brand_name', 'seller_id', 'seller_username']
    for col in label_encode_cols:
        if col in df.columns:
            le = LabelEncoder()
            df[col] = df[col].astype(str)
            df[col] = le.fit_transform(df[col])

    # One-hot encoding for product_type, product_category, product_season, product_gender_target, product_condition, seller_country
    one_hot_cols = [
        'product_type', 'product_category', 'product_season',
        'product_gender_target', 'product_condition', 'seller_country'
    ]
    one_hot_cols = [col for col in one_hot_cols if col in df.columns]
    df = pd.get_dummies(df, columns=one_hot_cols, drop_first=True)

    return df


def handle_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Placeholder for outlier detection and capping.
    For example, cap prices at 99th percentile.
    """
    if 'price_usd' in df.columns:
        upper_bound = df['price_usd'].quantile(0.99)
        df.loc[df['price_usd'] > upper_bound, 'price_usd'] = upper_bound

    # Similarly cap other numeric columns if needed
    return df


def scale_numeric_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Scale numeric features with StandardScaler.
    """
    numeric_cols = [
        'price_usd', 'seller_price', 'seller_earning',
        'seller_products_sold', 'seller_num_products_listed',
        'seller_num_followers', 'seller_pass_rate',
        'product_like_count'
    ]
    numeric_cols = [col for col in numeric_cols if col in df.columns]

    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    return df


def drop_unused_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop columns that are not useful for ML.
    """
    to_drop = [
        'brand_url', 'seller_badge', 'warehouse_name', 'seller_username',
        'product_description', 'product_keywords'  # Keep or drop depending on use case
    ]
    to_drop = [col for col in to_drop if col in df.columns]
    df = df.drop(columns=to_drop)
    return df


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full ML preprocessing pipeline.
    """
    df = advanced_impute_and_clean(df)
    df = text_processing(df)
    df = handle_outliers(df)
    df = encode_categoricals(df)
    df = scale_numeric_features(df)
    df = drop_unused_columns(df)
    return df


if __name__ == "__main__":
    # Example usage
    filepath = 'path_to_your_cleaned_data.csv'
    df = pd.read_csv(filepath)
    df_processed = preprocess(df)
    print(df_processed.head())
    