import pandas as pd


"""Data processing functions for the Fashion Resale project.
Loads, cleans, and prepares data for database insertion and machine learning."""

def load_raw_data(filepath: str) -> pd.DataFrame:
    """  Loads raw CSV data from the given filepath.
    low_memory = False - uses more memory but reads all document at once. By default it reads document by chunks. """
    df = pd.read_csv(filepath, low_memory=False)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """- Removing columns not usefull for SQL database and PowerBI insights.
    - Drop duplicates
    - If 'na' dropping rows
    -Maping product_type to category_group
    -Creating new brand_name group of others with less than 50 entries
    -Creating new product material group others for less than 1000 entries"""



    df = df.drop(columns=['product_id', 'product_name', 'product_description', 'product_keywords',
                          'product_like_count', 'reserved', 'should_be_gone',  'brand_id', 'brand_url',
                          'seller_badge', 'has_cross_border_fees', 'buyers_fees', 'warehouse_name',
                          'seller_id', 'seller_username', 'usually_ships_within',
                          'seller_community_rank', 'seller_num_followers', 'seller_pass_rate',])
    df = df.drop_duplicates()
    df = df.dropna(subset=['brand_name',  'product_material', 'product_season', 'product_color'])

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
    """"Fill product category NA values with "Other". Its most of the time Men or Women clothing."""
    df['product_category'] = df['product_category'].fillna('Other')

    '''Large amount of brands occure very little time
    Creating new brand entry Others for such cases'''
    # 1. Count frequency of each brand
    brand_counts = df['brand_name'].value_counts()
    # 2. Define threshold for rare brands
    threshold = 50
    # 3. Get all brands that appear less than threshold times
    rare_brands = brand_counts[brand_counts < threshold].index
    # 4. Replace rare brands with 'Other'
    df['brand_name'] = df['brand_name'].replace(rare_brands, 'Other')

    '''70 categories. With less than 1000 = 38 categories'''
    material_counts = df['product_material'].value_counts()
    threshold = 1000
    rare_materials = material_counts[material_counts < threshold].index
    df['product_material'] = df['product_material'].replace(rare_materials, 'Other')

    '''Converting Bool cols, not to get sting values'''
    bool_cols = ['sold', 'available', 'in_stock']
    for col in bool_cols:
        if col in df.columns:
            df[col] = df[col].astype(bool)

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
        'product_type',  # filtered to >=100 entries
        'category_group',  # new super-categories from product_type
        'brand_name',  # rare brands grouped as 'Other'
        'product_gender_target',  # Women / Men
        'product_category',  # 6 main categories, missing filled with 'Other'
        'product_season',  # Autumn/Winter, Spring/Summer
        'product_condition',  # 5 condition categories
        'sold',
        'available',
        'in_stock',
        'product_material',  # rare materials grouped as 'Other'
        'product_color',
        'price_usd',
        'seller_price',
        'seller_earning',
        'seller_country',
        'seller_products_sold',
        'seller_num_products_listed'
    ]

    return df[[col for col in columns_to_keep if col in df.columns]]


if __name__ == "__main__":
    filepath = 'path_to_your_raw_data.csv'
    df = load_raw_data(filepath)
    df = clean_data(df)
    df = select_final_columns(df)
