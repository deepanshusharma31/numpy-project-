# Task 7: Handling Missing Values
import os
import pandas as pd

pd.set_option("display.width", 160)
pd.set_option("display.max_columns", None)
BASE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(BASE, "data", "sales_data.csv"))

print("=== BEFORE handling missing values ===")
print("Shape:", df.shape)
print("\nisnull() on first 5 rows:\n", df.isnull().head())
print("\nMissing values per column:\n", df.isnull().sum())
print("Total missing cells:", df.isnull().sum().sum())
print("Rows with at least one missing value:", df.isnull().any(axis=1).sum())
print("\nRows containing missing values (sample):\n", df[df.isnull().any(axis=1)].head())

# Method 1: Drop rows
dropped = df.dropna()
print("\n=== Method 1: dropna() ===")
print("Shape after dropping rows:", dropped.shape, "-> rows lost:", len(df) - len(dropped))

# Method 2: Fill with appropriate values
filled = df.copy()
filled["quantity"] = filled["quantity"].fillna(filled["quantity"].median())              # median (count data)
filled["unit_price"] = filled["unit_price"].fillna(                                      # mean price of same product
    filled.groupby("product")["unit_price"].transform("mean").round(-1))
filled["discount"] = filled["discount"].fillna(0)                                        # assume no discount
filled["region"] = filled["region"].fillna(filled["region"].mode()[0])                   # most frequent region

print("\n=== Method 2: fillna() ===")
print("Missing values per column after filling:\n", filled.isnull().sum())
print("Shape after filling:", filled.shape, "(no rows lost)")
print("\nMedian used for quantity :", df["quantity"].median())
print("Mode used for region     :", df["region"].mode()[0])

print("\n=== AFTER: sample of rows that originally had gaps ===")
idx = df[df.isnull().any(axis=1)].index[:5]
print("Before:\n", df.loc[idx, ["order_id", "product", "quantity", "unit_price", "discount", "region"]])
print("After:\n", filled.loc[idx, ["order_id", "product", "quantity", "unit_price", "discount", "region"]])

print("""
Why handling missing data matters in Data Analytics:
 1. Missing values bias statistics (means, totals, correlations) and give wrong insights.
 2. Many functions/ML models fail or silently skip rows containing NaN.
 3. Dropping too much data shrinks the sample; filling sensibly keeps information.
 4. Clean, complete data makes dashboards and reports trustworthy.""")
