"""Generates the practice datasets used in Tasks 5-10 (run once)."""
import os
import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(42)

# ---- Customers -------------------------------------------------------------
first = ["Aarav","Vivaan","Ananya","Diya","Rohan","Isha","Kabir","Meera","Arjun","Sana",
         "Ishaan","Riya","Kunal","Neha","Aditya","Pooja","Varun","Simran","Nikhil","Tanvi"]
last = ["Sharma","Verma","Gupta","Singh","Mehta","Khan","Patel","Reddy","Nair","Das"]
cities = ["Delhi","Mumbai","Bengaluru","Kolkata","Chennai","Hyderabad","Pune","Jaipur"]
segments = ["Consumer","Corporate","Home Office"]
customers = pd.DataFrame({
    "customer_id": range(1, 51),
    "customer_name": [f"{rng.choice(first)} {rng.choice(last)}" for _ in range(50)],
    "city": rng.choice(cities, 50),
    "segment": rng.choice(segments, 50, p=[0.55, 0.30, 0.15]),
})
customers.to_csv(os.path.join(BASE, "data", "customers.csv"), index=False)

# ---- Sales (with deliberately injected missing values) ----------------------
catalog = {
    "Laptop": ("Electronics", 55000), "Smartphone": ("Electronics", 22000),
    "Headphones": ("Electronics", 3000), "T-Shirt": ("Clothing", 800),
    "Jeans": ("Clothing", 1800), "Sneakers": ("Footwear", 3500),
    "Backpack": ("Accessories", 1500), "Watch": ("Accessories", 4500),
    "Notebook": ("Stationery", 120), "Pen Set": ("Stationery", 250),
}
n = 200
products = rng.choice(list(catalog), n, p=[.06,.10,.14,.14,.10,.10,.10,.06,.12,.08])
sales = pd.DataFrame({
    "order_id": range(1001, 1001 + n),
    "order_date": pd.to_datetime("2026-01-01") + pd.to_timedelta(rng.integers(0, 180, n), unit="D"),
    "customer_id": rng.integers(1, 51, n),
    "product": products,
    "category": [catalog[p][0] for p in products],
    "quantity": rng.integers(1, 6, n).astype(float),
    "unit_price": [round(catalog[p][1] * rng.uniform(0.95, 1.05), -1) for p in products],
    "discount": rng.choice([0, 0.05, 0.10, 0.15], n, p=[.45, .25, .2, .1]),
    "region": rng.choice(["North", "South", "East", "West"], n),
    "payment_mode": rng.choice(["UPI", "Credit Card", "Debit Card", "Cash"], n, p=[.45,.25,.2,.1]),
})
sales["order_date"] = sales["order_date"].dt.strftime("%Y-%m-%d")
sales = sales.sort_values("order_date").reset_index(drop=True)
sales["order_id"] = range(1001, 1001 + n)

for col, frac in [("quantity", .06), ("unit_price", .05), ("discount", .05), ("region", .04)]:
    idx = rng.choice(n, int(n * frac), replace=False)
    sales.loc[idx, col] = np.nan
sales.to_csv(os.path.join(BASE, "data", "sales_data.csv"), index=False)
print("Datasets created:", customers.shape, sales.shape)
