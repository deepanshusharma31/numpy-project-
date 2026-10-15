# Task 9: Exporting Data
import os
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(BASE, "data", "sales_data.csv"))

# Process the dataset
df["quantity"] = df["quantity"].fillna(df["quantity"].median())
df["unit_price"] = df["unit_price"].fillna(df.groupby("product")["unit_price"].transform("mean").round(-1))
df["discount"] = df["discount"].fillna(0)
df["region"] = df["region"].fillna(df["region"].mode()[0])
df["revenue"] = (df["quantity"] * df["unit_price"] * (1 - df["discount"])).round(2)

out_path = os.path.join(BASE, "output", "processed_sales_data.csv")
df.to_csv(out_path, index=False)
print("Exported to:", out_path)

# Verify the exported file
check = pd.read_csv(out_path)
print("\nVerification - re-read exported file:")
print("Shape            :", check.shape)
print("Columns          :", list(check.columns))
print("Missing values   :", int(check.isnull().sum().sum()))
print("Matches in-memory data (values):", bool((check.drop(columns='order_date').round(2).equals(df.drop(columns='order_date').round(2)))))
print("\nFirst 5 rows of exported file:\n", check.head().to_string())
