# Task 10: Mini Data Analysis Project - Sales Performance Analysis (NumPy + Pandas)
import os
import numpy as np
import pandas as pd

pd.set_option("display.width", 160)
pd.set_option("display.max_columns", None)
BASE = os.path.dirname(os.path.abspath(__file__))

# 1. LOAD ----------------------------------------------------------------------
sales = pd.read_csv(os.path.join(BASE, "data", "sales_data.csv"), parse_dates=["order_date"])
customers = pd.read_csv(os.path.join(BASE, "data", "customers.csv"))
print("1. LOADED: sales", sales.shape, "| customers", customers.shape)

# 2. INSPECT -------------------------------------------------------------------
print("\n2. INSPECTION")
print(sales.head(3))
print("\nDtypes:\n", sales.dtypes)
print("\nMissing values:\n", sales.isnull().sum()[sales.isnull().sum() > 0])
print("Duplicate order_ids:", sales["order_id"].duplicated().sum())

# 3. HANDLE MISSING VALUES -----------------------------------------------------
sales["quantity"] = sales["quantity"].fillna(sales["quantity"].median())
sales["unit_price"] = sales["unit_price"].fillna(sales.groupby("product")["unit_price"].transform("mean").round(-1))
sales["discount"] = sales["discount"].fillna(0)
sales["region"] = sales["region"].fillna(sales["region"].mode()[0])
print("\n3. After cleaning, total missing values:", int(sales.isnull().sum().sum()))

# Feature engineering (NumPy + Pandas)
sales["revenue"] = np.round(sales["quantity"] * sales["unit_price"] * (1 - sales["discount"]), 2)
sales["month"] = sales["order_date"].dt.month_name()
sales["month_no"] = sales["order_date"].dt.month
sales["order_size"] = np.where(sales["revenue"] >= sales["revenue"].median(), "Large", "Small")
df = sales.merge(customers, on="customer_id", how="left")

# 4. SELECT & FILTER -----------------------------------------------------------
print("\n4. SELECT & FILTER")
high_value = df[df["revenue"] > 100000]
print("Orders with revenue > Rs 1,00,000:", len(high_value))
print(high_value[["order_id", "product", "city", "revenue"]].head())
upi_big = df[(df["payment_mode"] == "UPI") & (df["discount"] >= 0.10)]
print("UPI orders with >=10% discount:", len(upi_big))

# 5. SORT ----------------------------------------------------------------------
print("\n5. TOP 5 ORDERS BY REVENUE")
print(df.sort_values("revenue", ascending=False)[["order_id", "product", "city", "quantity", "revenue"]].head())

# 6. GROUPBY -------------------------------------------------------------------
print("\n6. GROUPBY ANALYSIS")
by_product = df.groupby("product").agg(revenue=("revenue", "sum"), units=("quantity", "sum"),
                                       orders=("order_id", "count")).sort_values("revenue", ascending=False)
by_product["revenue_share_%"] = (by_product["revenue"] / by_product["revenue"].sum() * 100).round(1)
print("Revenue by product:\n", by_product.round(0))
by_cat = df.groupby("category")["revenue"].sum().sort_values(ascending=False)
by_region = df.groupby("region")["revenue"].sum().sort_values(ascending=False)
by_city = df.groupby("city")["revenue"].sum().sort_values(ascending=False)
by_seg = df.groupby("segment").agg(revenue=("revenue", "sum"), avg_order=("revenue", "mean"))
by_pay = df.groupby("payment_mode")["order_id"].count().sort_values(ascending=False)
by_month = df.groupby(["month_no", "month"])["revenue"].sum()
print("\nRevenue by category:\n", by_cat.round(0))
print("\nRevenue by region:\n", by_region.round(0))
print("\nTop 3 cities:\n", by_city.head(3).round(0))
print("\nSegment summary:\n", by_seg.round(0))
print("\nOrders by payment mode:\n", by_pay)
print("\nMonthly revenue:\n", by_month.round(0))
disc = df.groupby("discount")["quantity"].mean().round(2)
print("\nAvg quantity per order by discount level:\n", disc)

# 7. PIVOT TABLES --------------------------------------------------------------
print("\n7. PIVOT TABLES")
pv1 = pd.pivot_table(df, values="revenue", index="category", columns="region", aggfunc="sum",
                     fill_value=0, margins=True, margins_name="Total").round(0)
print("Revenue: category x region\n", pv1)
pv2 = pd.pivot_table(df, values="revenue", index=["month_no", "month"], columns="category",
                     aggfunc="sum", fill_value=0).round(0)
print("\nRevenue: month x category\n", pv2)

# 8. NUMPY STATISTICS ----------------------------------------------------------
rev = df["revenue"].to_numpy()
print("\n8. NUMPY STATS on revenue")
print("Mean:", round(float(np.mean(rev)), 2), "| Median:", round(float(np.median(rev)), 2),
      "| Std:", round(float(np.std(rev)), 2))
print("90th percentile:", round(float(np.percentile(rev, 90)), 2))
top20 = df.sort_values("revenue", ascending=False).head(int(0.2 * len(df)))["revenue"].sum()
print("Top 20% of orders generate", round(top20 / rev.sum() * 100, 1), "% of total revenue")
print("Total revenue:", round(float(rev.sum()), 2))

# 9. EXPORT --------------------------------------------------------------------
out = os.path.join(BASE, "output", "cleaned_sales_project.csv")
df.drop(columns=["month_no"]).to_csv(out, index=False)
print("\n9. EXPORTED cleaned dataset ->", out, "| shape:", df.drop(columns=['month_no']).shape)
