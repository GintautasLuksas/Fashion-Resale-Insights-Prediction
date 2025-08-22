import pandas as pd
import numpy as np


"""Data processing functions for the Fashion Resale project.
Loads, cleans, and prepares data for database insertion and machine learning."""

def load_raw_data(filepath: str) -> pd.DataFrame:
    """  Loads raw CSV data from the given filepath.
    low_memory = False - uses more memory but reads all document at once. By default it reads document by chunks. """
    df = pd.read_csv(filepath, low_memory=False)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """- Drops duplicates.
    - Removes reserved and should be gone columns. (no valuable data can be estracted)
    - Removes rows with missing essential data (brand)"""

    df = df.drop_duplicates()
    df = df.drop(columns=['reserved', 'should_be_gone'])
    df = df.dropna(subset=['brand_name'])

    """"Dropping any rows that has less than 100 entries in product_type category"""
    product_counts = df['product_type'].value_counts()
    valid_products = product_counts[product_counts >= 100].index
    df = df[df['product_type'].isin(valid_products)].copy()

    return df


def impute_price_median(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fills missing price_usd with the median price of sold items.

    Parameters:
        df (pd.DataFrame): Dataset after initial cleaning.

    Returns:
        pd.DataFrame: Dataset with missing prices imputed.
    """
    median_price_sold = df.loc[df['sold'] == True, 'price_usd'].median()

    mask_missing_price = df['price_usd'].isna()
    df.loc[mask_missing_price & (df['sold'] == True), 'price_usd'] = median_price_sold

    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
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

    df['brand_encoded'] = df['brand_name'].astype('category').cat.codes
    df['condition_encoded'] = df['product_condition'].astype('category').cat.codes
    df['gender_encoded'] = df['product_gender_target'].astype('category').cat.codes

    return df


def select_final_columns(df: pd.DataFrame) -> pd.DataFrame:
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
    return df[[col for col in columns_to_keep if col in df.columns]]


def encode_categoricals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Placeholder for future encoding steps.

    Parameters:
        df (pd.DataFrame): Dataset to encode.

    Returns:
        pd.DataFrame: Currently unchanged.
    """
    return df


# Example pipeline usage:
if __name__ == "__main__":
    filepath = 'path_to_your_raw_data.csv'
    df = load_raw_data(filepath)
    df = clean_data(df)
    df = impute_price_median(df)
    df = engineer_features(df)
    df = select_final_columns(df)
    df = encode_categoricals(df)
    # Now df is ready for export or further analysis
