"""Clean the raw data with pandas and save data/superstore_clean.csv"""
import pandas as pd

try:
    df = pd.read_csv("data/superstore_raw.csv")
except UnicodeDecodeError:                       # the real Kaggle file is latin-1 encoded
    df = pd.read_csv("data/superstore_raw.csv", encoding="latin-1")

print("Raw shape:", df.shape)
print("Missing values:\n", df.isna().sum()[df.isna().sum() > 0])
print("Duplicate rows:", df.duplicated().sum())

df.columns = df.columns.str.strip()
df = df.drop_duplicates()

for c in df.select_dtypes(include=["object", "string"]):
    df[c] = df[c].str.strip()
df["Customer Name"] = df["Customer Name"].str.title()
df["Segment"] = df["Segment"].fillna("Unknown")

df["Order Date"] = pd.to_datetime(df["Order Date"], format="mixed")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="mixed")

# feature engineering
df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month
df["Year-Month"] = df["Order Date"].dt.strftime("%Y-%m")
df["Ship Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
df["Profit Margin %"] = (df["Profit"] / df["Sales"] * 100).round(2)

df.to_csv("data/superstore_clean.csv", index=False)
print("Clean shape:", df.shape, "-> saved data/superstore_clean.csv")
