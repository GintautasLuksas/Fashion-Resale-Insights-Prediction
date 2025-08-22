import pandas as pd

# Load your dataset
file_path = r"C:\Users\user\PycharmProjects\Fashion-Resale-Insights-Prediction\data\raw\vestiaire.csv"
df = pd.read_csv(file_path)

# 1. Display number of non-null (filled) entries for each column
# print("Non-null counts per column:")
# print(df.notnull().sum())
#
# # 2. Percentage completeness for each column
# print("\nPercentage of non-null values per column:")
# print((df.notnull().sum() / len(df) * 100).round(2))
#
# # 3. Number of unique values per column
# unique_counts = df.nunique()
# print("\nUnique values per column:")
# print(unique_counts.sort_values(ascending=False))

# 4. Inspect unique values for boolean-like columns
bool_columns = ['sold', 'reserved', 'available', 'in_stock', 'should_be_gone']

# for col in bool_columns:
#     if col in df.columns:
#         print(f"\n--- {col} ---")
#         print("Unique values:", df[col].unique())
#         print("\nValue counts:")
#         print(df[col].value_counts(dropna=False))


import pandas as pd

# Load your dataset
file_path = r"C:\Users\user\PycharmProjects\Fashion-Resale-Insights-Prediction\data\raw\vestiaire.csv"
df = pd.read_csv(file_path, low_memory=False)

# Filter only sold items
sold_items = df[df['sold'] == False]

# Get counts of each product_type
product_counts = sold_items['product_type'].value_counts()

# Save to TXT file
txt_path = r"C:\Users\user\PycharmProjects\Fashion-Resale-Insights-Prediction\data\raw\product_keywords_not_sold.txt"
with open(txt_path, 'w', encoding='utf-8') as f:
    for product, count in product_counts.items():
        f.write(f"{product}: {count}\n")

print(f"File saved to {txt_path}")


# Check unique values for product_gender_target
if 'product_gender_target' in df.columns:
    print("\n--- product_gender_target ---")
    print("Unique values:", df['product_gender_target'].unique())
    print("Value counts:")
    print(df['product_gender_target'].value_counts(dropna=False))

# Check unique values for product_category
if 'product_category' in df.columns:
    print("\n--- product_category ---")
    print("Unique values:", df['product_category'].unique())
    print("Value counts:")
    print(df['product_category'].value_counts(dropna=False))


