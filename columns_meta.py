import pandas as pd

df = pd.read_csv("retail_sales_dataset.csv")
print(df.head())
print("\nColumns:", df.columns.tolist())
print("\nInfo:")
print(df.info())
