# Task 5: Reading & Inspecting Data
import os
import pandas as pd

pd.set_option("display.width", 160)
pd.set_option("display.max_columns", None)
BASE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(BASE, "data", "sales_data.csv"))

print("First 5 rows (head):\n", df.head())
print("\nLast 5 rows (tail):\n", df.tail())
print("\nShape (rows, columns):", df.shape)
print("Number of rows   :", df.shape[0])
print("Number of columns:", df.shape[1])
print("\nColumn names:", list(df.columns))
print("\nData types (dtypes):\n", df.dtypes)
print("\ninfo():")
df.info()
print("\ndescribe():\n", df.describe().round(2))
