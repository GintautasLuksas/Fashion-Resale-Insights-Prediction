import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler

def clean_for_ml(df):
    df = df.copy()

    # 1. Drop ID-like or constant columns
    drop_cols = [
        "product_id", "seller_id", "brand_id", "brand_url", "seller_username",
        "reserved", "has_cross_border_fees"
    ]
    drop_cols = [c for c in drop_cols if c in df.columns]
    df.drop(columns=drop_cols, inplace=True)

    # 2. Binary features → 0/1 integers
    binary_cols = [
        "in_stock", "sold", "available", "should_be_gone", "product_gender_target"
    ]
    for col in binary_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.lower().map(
                {"true": 1, "false": 0, "1": 1, "0": 0}
            ).fillna(0).astype(int)

    # 3. Fill missing values
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna("Unknown")
        else:
            df[col] = df[col].fillna(df[col].median())

    # 4. Separate categorical and numeric
    cat_cols = df.select_dtypes(include=["object"]).columns.tolist()
    num_cols = df.select_dtypes(exclude=["object"]).columns.tolist()

    # 5. One-hot encode low-cardinality categorical features
    low_card_cat = [c for c in cat_cols if df[c].nunique() <= 20]
    high_card_cat = [c for c in cat_cols if df[c].nunique() > 20]

    if low_card_cat:
        encoder = OneHotEncoder(sparse_output=False, drop="first")
        encoded = encoder.fit_transform(df[low_card_cat])
        encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(low_card_cat))
        df = pd.concat([df.drop(columns=low_card_cat), encoded_df], axis=1)

    # 6. Frequency encode high-cardinality categorical features
    for col in high_card_cat:
        freq_map = df[col].value_counts(normalize=True).to_dict()
        df[col] = df[col].map(freq_map)

    # 7. Standard scale numeric columns
    scaler = StandardScaler()
    df[num_cols] = scaler.fit_transform(df[num_cols])

    return df


# ------------------------
# Load, clean, and save
# ------------------------
input_path = r"C:\Users\user\PycharmProjects\Fashion-Resale-Insights-Prediction\data\raw\vestiaire.csv"
output_path = r"C:\Users\user\PycharmProjects\Fashion-Resale-Insights-Prediction\data\processed\cleaned_data.csv"

df = pd.read_csv(input_path)
df_clean = clean_for_ml(df)

df_clean.to_csv(output_path, index=False)

print(f"✅ Cleaned dataset saved to {output_path}")
print(f"Shape: {df_clean.shape}")
