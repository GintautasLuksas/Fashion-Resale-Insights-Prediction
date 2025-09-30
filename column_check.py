import pandas as pd

# Load dataset
file_path = r"C:\Users\user\PycharmProjects\Fashion-Resale-Insights-Prediction\data\raw\vestiaire.csv"
df = pd.read_csv(file_path, low_memory=False)

# Columns to keep for SQL
keep_cols = [
    'product_type',
    'product_gender_target',
    'product_category',
    'product_season',
    'product_condition',
    'sold',
    'available',
    'in_stock',
    'brand_name',
    'product_material',
    'product_color',
    'price_usd',
    'seller_price',
    'seller_earning',
    'seller_country',
    'available',
    'in_stock',
    'reserved'
]

# 1. Null counts + percentage
null_summary = pd.DataFrame({
    "Null_Count": df[keep_cols].isnull().sum(),
    "Null_Percent": (df[keep_cols].isnull().sum() / len(df) * 100).round(2)
}).sort_values(by="Null_Count", ascending=False)

print("\n--- Missing Values Summary ---")
print(null_summary)

# 2. Show unique values + counts for categorical columns
categorical_cols = [
    'product_gender_target',
    'product_category',
    'product_season',
    'product_condition',
    'brand_name',
    'product_material',
    'product_color',
    'seller_country',
    'reserved',
    'available',
    'in_stock',
    'should_be_gone',
    'seller_badge',
    'has_cross_border_fees',
    'buyers_fees',
    'warehouse_name',
    'usually_ships_within',
    'seller_num_followers',
'seller_pass_rate',
'product_like_count'
]

for col in categorical_cols:
    if col in df.columns:
        print(f"\n--- {col} ---")
        print("Unique values:", df[col].dropna().unique()[:10], "...")  # show first 10
        print("Unique count:", df[col].nunique())
        print("Value counts (top 10):")
        print(df[col].value_counts(dropna=False).head(10))




# Brand frequency counts
brand_counts = df['product_material'].value_counts()

# Count how many brands have less than 50 entries
brands_under_50 = (brand_counts < 1000).sum()

# Total number of brands
total_brands = df['product_material'].nunique()

# Share of small brands
percentage = (brands_under_50 / total_brands) * 100

print(f"Brands with <50 entries: {brands_under_50} out of {total_brands} ({percentage:.2f}%)")


df['price_usd'].isnull().sum()