import pandas as pd

# Load your dataset
file_path = r"C:\Users\user\PycharmProjects\Fashion-Resale-Insights-Prediction\data\raw\vestiaire.csv"
df = pd.read_csv(file_path)

# Display number of non-null (filled) entries for each column
print(df.notnull().sum())

# Also see percentage completeness for each column
print("\nPercentage of non-null values per column:")
print((df.notnull().sum() / len(df) * 100).round(2))

unique_counts = df.nunique()

print("Unique values per column:")
print(unique_counts.sort_values(ascending=False))
