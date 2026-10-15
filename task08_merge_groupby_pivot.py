# Task 8: Merge, Concatenate, GroupBy & Pivot Table
import os
import pandas as pd

pd.set_option("display.width", 160)
pd.set_option("display.max_columns", None)
BASE = os.path.dirname(os.path.abspath(__file__))
sales = pd.read_csv(os.path.join(BASE, "data", "sales_data.csv"))
customers = pd.read_csv(os.path.join(BASE, "data", "customers.csv"))

# Quick clean so aggregates are meaningful
sales["quantity"] = sales["quantity"].fillna(sales["quantity"].median())
sales["unit_price"] = sales["unit_price"].fillna(sales.groupby("product")["unit_price"].transform("mean"))
sales["discount"] = sales["discount"].fillna(0)
sales["region"] = sales["region"].fillna("Unknown")
sales["revenue"] = sales["quantity"] * sales["unit_price"] * (1 - sales["discount"])

print("=== MERGE: sales + customers on 'customer_id' ===")
merged = pd.merge(sales, customers, on="customer_id", how="left")
print(merged[["order_id", "customer_id", "customer_name", "city", "segment", "product", "revenue"]].head())
print("Shape after merge:", merged.shape)

print("\n=== CONCATENATE: first 100 orders + last 100 orders (stack rows) ===")
part1, part2 = sales.iloc[:100], sales.iloc[100:]
combined = pd.concat([part1, part2], ignore_index=True)
print("part1:", part1.shape, "| part2:", part2.shape, "| combined:", combined.shape)
side = pd.concat([sales[["order_id", "product"]].head(3), sales[["quantity", "revenue"]].head(3)], axis=1)
print("Column-wise concat (axis=1):\n", side)

print("\n=== GROUPBY: revenue by category ===")
print(merged.groupby("category")["revenue"].sum().round(0).sort_values(ascending=False))

print("\n=== GROUPBY: multiple aggregates by region ===")
agg = merged.groupby("region").agg(
    total_revenue=("revenue", "sum"),
    avg_revenue=("revenue", "mean"),
    orders=("order_id", "count"),
    min_qty=("quantity", "min"),
    max_qty=("quantity", "max"),
).round(0)
print(agg)

print("\n=== GROUPBY: average revenue by customer segment ===")
print(merged.groupby("segment")["revenue"].mean().round(0))

print("\n=== PIVOT TABLE: total revenue (rows=category, columns=region) ===")
pivot = pd.pivot_table(merged, values="revenue", index="category", columns="region",
                       aggfunc="sum", fill_value=0, margins=True, margins_name="Total").round(0)
print(pivot)

print("\n=== PIVOT TABLE: avg quantity (rows=segment, columns=payment_mode) ===")
print(pd.pivot_table(merged, values="quantity", index="segment", columns="payment_mode",
                     aggfunc="mean").round(2))
