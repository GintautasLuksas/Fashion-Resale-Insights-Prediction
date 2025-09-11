import pandas as pd


csv_path = r'C:\Users\user\PycharmProjects\Fashion-Resale-Insights-Prediction\data\processed\vestiaire_processed.csv'
excel_path = r'C:\Users\user\PycharmProjects\Fashion-Resale-Insights-Prediction\data\processed\vestiaire_sample.xlsx'
df = pd.read_csv(csv_path)

df_sample = df.head(1000)
df_sample.to_excel(excel_path, index=False)

print(f"✅ Excel file saved: {excel_path}")
