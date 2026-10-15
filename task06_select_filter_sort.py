# Task 6: Selecting, Filtering & Sorting Data
import os
import pandas as pd

pd.set_option("display.width", 150)
BASE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(BASE, "data", "sales_data.csv"))

print("--- Select specific columns ---")
print(df[["order_id", "product", "quantity", "unit_price"]].head())

print("\n--- Select specific rows ---")
print("df.iloc[5:10]:\n", df.iloc[5:10][["order_id", "product", "region"]])
print("df.loc[0:2, ['order_id','product']]:\n", df.loc[0:2, ["order_id", "product"]])

print("\n--- Filter: unit_price > 20000 ---")
expensive = df[df["unit_price"] > 20000]
print(expensive[["order_id", "product", "unit_price"]].head())
print("Matching rows:", len(expensive))

print("\n--- Multiple conditions: Electronics AND region == 'North' AND quantity >= 3 ---")
multi = df[(df["category"] == "Electronics") & (df["region"] == "North") & (df["quantity"] >= 3)]
print(multi[["order_id", "product", "region", "quantity", "unit_price"]])

print("\n--- OR condition + isin: payment_mode is UPI or Cash ---")
print(df[df["payment_mode"].isin(["UPI", "Cash"])][["order_id", "payment_mode"]].head())

print("\n--- Sort ascending by unit_price (top 5) ---")
print(df.sort_values("unit_price", ascending=True)[["order_id", "product", "unit_price"]].head())

print("\n--- Sort descending by unit_price (top 5) ---")
print(df.sort_values("unit_price", ascending=False)[["order_id", "product", "unit_price"]].head())

print("\n--- Sort by two columns: category (A-Z), then quantity (high-low) ---")
print(df.sort_values(["category", "quantity"], ascending=[True, False])[["category", "product", "quantity"]].head(8))
