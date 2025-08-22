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
    df = df.drop(columns=['product_id', 'product_name', 'product_description', 'product_keywords'
                          'product_like_count', 'reserved', 'should_be_gone',  'brand_id', 'brand_url',
                          'seller_id', 'seller_username', 'usually_ships_within', 'seller_products_sold',
                          'seller_num_products_listed', 'seller_community_rank', 'seller_num_followers',
                          'seller_pass_rate'])
    df = df.dropna(subset=['brand_name'])

    """"Dropping any rows that has less than 100 entries in product_type category"""
    product_counts = df['product_type'].value_counts()
    valid_products = product_counts[product_counts >= 100].index
    df = df[df['product_type'].isin(valid_products)].copy()

    """- Maps detailed product_type entries into broader, high-level categories for easier analysis.
    - Original `product_type` is preserved for detailed views or later ML/NLP work.
    - New column `category_group` is created with simplified groups such as:
        - Clothing
        - Footwear
        - Accessories
        - Bags
        - Intimates & Swimwear
        - Other
    - Any product_type not explicitly mapped is assigned to 'Other'. """

    group_map = {
        'T-shirt': 'Clothing', 'Shirt': 'Clothing', 'Polo shirt': 'Clothing',
        'Sweatshirt': 'Clothing', 'Top': 'Clothing', 'Vest': 'Clothing',
        'Blouse': 'Clothing', 'Dress': 'Clothing', 'Mini dress': 'Clothing',
        'Mid-length dress': 'Clothing', 'Maxi dress': 'Clothing',
        'Skirt': 'Clothing', 'Mini skirt': 'Clothing', 'Mid-length skirt': 'Clothing',
        'Trousers': 'Clothing', 'Jeans': 'Clothing', 'Slim jeans': 'Clothing',
        'Straight jeans': 'Clothing', 'Shorts': 'Clothing', 'Leggings': 'Clothing',
        'Suit': 'Clothing', 'Suit jacket': 'Clothing', 'Blazer': 'Clothing',
        'Coat': 'Clothing', 'Wool coat': 'Clothing', 'Trench coat': 'Clothing',
        'Jacket': 'Clothing', 'Leather jacket': 'Clothing', 'Wool jacket': 'Clothing',
        'Pull': 'Clothing', 'Wool pull': 'Clothing', 'Cardigan': 'Clothing',

        'Boots': 'Footwear', 'Leather boots': 'Footwear',
        'Heels': 'Footwear', 'Leather heels': 'Footwear', 'Patent leather heels': 'Footwear',
        'Flats': 'Footwear', 'Leather flats': 'Footwear', 'Ballet flats': 'Footwear',
        'Sandals': 'Footwear', 'Leather sandals': 'Footwear', 'Leather mules': 'Footwear',
        'Trainers': 'Footwear', 'Leather trainers': 'Footwear',
        'Low trainers': 'Footwear', 'Cloth trainers': 'Footwear',
        'Mules & clogs': 'Footwear',

        'Sunglasses': 'Accessories', 'Watch': 'Accessories',
        'Belt': 'Accessories', 'Leather belt': 'Accessories',
        'Hat': 'Accessories', 'Scarf': 'Accessories', 'Tie': 'Accessories',
        'Silk tie': 'Accessories', 'Gloves': 'Accessories', 'Jewellery': 'Accessories',

        'Bag': 'Bags', 'Clutch': 'Bags', 'Backpack': 'Bags',
        'Handbag': 'Bags', 'Shoulder bag': 'Bags', 'Tote': 'Bags',

        'Lingerie': 'Intimates & Swimwear', 'Silk lingerie set': 'Intimates & Swimwear',
        'Bra': 'Intimates & Swimwear', 'Underwear': 'Intimates & Swimwear',
        'Swimwear': 'Intimates & Swimwear', 'Bikini': 'Intimates & Swimwear',

        'Wallet': 'Other', 'Cufflinks': 'Other', 'Home textile': 'Other'
    }

    df['category_group'] = df['product_type'].map(group_map).fillna('Other')
    """"Fill product category NA values with "Other". Its most of the time Me or Women clothing."""
    df['product_category'] = df['product_category'].fillna('Other')

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
