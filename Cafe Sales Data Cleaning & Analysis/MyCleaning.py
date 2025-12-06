import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =============================================================
# 1. LOAD DATA
# =============================================================

df = pd.read_csv("dirty_cafe_sales.csv")
df_clean = df.copy()

# =============================================================
# 2. CLEAN COLUMN NAMES
# =============================================================

df_clean.columns = (
    df_clean.columns
    .str.strip()
    .str.replace(" ", "_")
    .str.lower()
)

# =============================================================
# 3. REPLACE INVALID VALUES WITH NaN
# =============================================================

invalid_strings = ["ERROR", "UNKNOWN", "", "nan", "NaN", "None", "N/A"]

cols_to_clean = [
    "quantity", "price_per_unit", "item",
    "total_spent", "payment_method",
    "location", "transaction_date"
]

df_clean[cols_to_clean] = df_clean[cols_to_clean].replace(invalid_strings, np.nan)

# =============================================================
# 4. FIX DATA TYPES
# =============================================================

text_cols = ["transaction_id", "item", "payment_method", "location"]
for col in text_cols:
    df_clean[col] = df_clean[col].astype(str).str.strip()

numeric_cols = ["quantity", "price_per_unit", "total_spent"]
for col in numeric_cols:
    df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")

df_clean["transaction_date"] = pd.to_datetime(df_clean["transaction_date"], errors="coerce")

df_clean["year"] = df_clean["transaction_date"].dt.year
df_clean["month"] = df_clean["transaction_date"].dt.month
df_clean["day_of_week"] = df_clean["transaction_date"].dt.dayofweek

# =============================================================
# 5. FILL MISSING ITEM / PRICE USING MAP LOGIC
# =============================================================

price_dict = {
    'Coffee': 2.0, 'Tea': 1.5, 'Sandwich': 4.0,
    'Salad': 5.0, 'Cake': 3.0, 'Cookie': 1.0,
    'Smoothie': 4.0, 'Juice': 3.0
}

df_clean["price_per_unit"] = df_clean["price_per_unit"].fillna(
    df_clean["item"].map(price_dict)
)

price_to_name = {
    2.0: 'Coffee', 1.5: 'Tea', 5.0: 'Salad', 1.0: 'Cookie'
}

df_clean["item"] = df_clean["item"].fillna(
    df_clean["price_per_unit"].map(price_to_name)
)

# =============================================================
# 6. FILL USING FORMULAS
# =============================================================

mask_total = df_clean["total_spent"].isna() & df_clean["quantity"].notna() & df_clean["price_per_unit"].notna()
df_clean.loc[mask_total, "total_spent"] = (
    df_clean.loc[mask_total, "quantity"] * df_clean.loc[mask_total, "price_per_unit"]
)

mask_quantity = df_clean["quantity"].isna() & df_clean["total_spent"].notna() & df_clean["price_per_unit"].notna()
df_clean.loc[mask_quantity, "quantity"] = (
    df_clean.loc[mask_quantity, "total_spent"] / df_clean.loc[mask_quantity, "price_per_unit"]
)

mask_price = df_clean["price_per_unit"].isna() & df_clean["quantity"].notna() & df_clean["total_spent"].notna()
df_clean.loc[mask_price, "price_per_unit"] = (
    df_clean.loc[mask_price, "total_spent"] / df_clean.loc[mask_price, "quantity"]
)

# =============================================================
# 7. FILL REMAINING NaN WITH MEAN (NUMERIC ONLY)
# =============================================================

df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].mean())

# =============================================================
# 8. REMOVE ROWS WITH INVALID TEXT (nan, None, "", null)
# =============================================================

bad_strings = [
    "nan", "NaN", "NAN", "none", "None", "NONE",
    "null", "Null", "NULL", ""
]

text_columns = ["item", "payment_method", "location"]
for col in text_columns:
    df_clean[col] = df_clean[col].replace(bad_strings, np.nan)

df_clean = df_clean.dropna(subset=["item", "payment_method", "location", "transaction_date"])

# =============================================================
# 9. OPTIONAL SAVE
# =============================================================

#df_clean.to_csv("clean_cafe_sales.csv", index=False)


# =============================================================
# 10. EDA – Exploratory Data Analysis
# =============================================================
# Qëllimi: të kuptojmë datasetin me statistika, counts, dhe totalet.

"""

# --- Statistikat bazë të kolonave numerike ---
print(df_clean[["quantity", "price_per_unit", "total_spent"]].describe())

# Llogarit numrin e artikujve të shitur
print(df_clean["item"].count())
print(df_clean["item"].unique())
print(df_clean["item"].value_counts())  # Sa herë është shitur secili artikull

# Llogarit metodat e pagesës
print(df_clean["payment_method"].value_counts())
df_clean.groupby("payment_method")["total_spent"].sum()

# Llogarit shitjet sipas lokacionit
print(df_clean["location"].value_counts())
df_clean.groupby("location")["total_spent"].sum()

# Shitjet totale për secilin artikull
print(df_clean.groupby("item")["total_spent"].sum())

# Shitjet sipas ditës së javës
print(df_clean.groupby("day_of_week")["total_spent"].sum())

# Shitjet sipas muajit
print(df_clean.groupby("month")["total_spent"].sum())

# Shitjet sipas vitit
print(df_clean.groupby("year")["total_spent"].sum())

"""

# =============================================================
# 11. Vizualizimi
# =============================================================


# 1. Bar Charts
# A
"""
total_sales = df_clean.groupby('item')['total_spent'].sum()

x = list(total_sales.index)
y = list(total_sales.values)

plt.bar(x, y)

plt.xticks(rotation=45, ha='right')

plt.title("Total Sales per Item")
plt.xlabel("Item")
plt.ylabel("Total Sales")

plt.tight_layout()

plt.show()
"""
# B
payments = df_clean["payment_method"].value_counts()

x = list(payments.index)
y = list(payments.values)

plt.figure(figsize=(8,5))

# Ngjyra të personalizuara për çdo metodë pagese
colors = ["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#CCB974"]

# Shtyllat
bars = plt.bar(x, y, color=colors[:len(x)], width=0.55, edgecolor="black", linewidth=1.2)

# Titulli dhe fontet
plt.title("Count of Payment Methods", fontsize=16, fontweight="bold", pad=15)
plt.xlabel("Payment Method", fontsize=13)
plt.ylabel("Count", fontsize=13)

# Vendos një grid horizontal të butë
plt.grid(axis="y", linestyle="--", alpha=0.4)

# Vendos etiketa mbi shtyllat
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2,
        height + 0.3,
        str(height),
        ha='center',
        va='bottom',
        fontsize=12,
        fontweight="bold"
    )

plt.tight_layout()
plt.show()

#2.
