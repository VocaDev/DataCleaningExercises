import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# =============================================================
# 1. NGARKIMI I TE DHENAVE
# =============================================================

df = pd.read_csv("dirty_cafe_sales.csv")

# Krijojmë një kopje që të mos prekim datasetin origjinal
df_clean = df.copy()


# =============================================================
# 2. KORRIGJIMI I EMRAVE TË KOLONAVE
# =============================================================
# Qëllimi:
# - të largojmë hapësirat në emra
# - t’i konvertojmë në lowercase
# - t’i bëjmë më të lehtë për t’u përdorur në analiza / programim

df_clean.columns = df_clean.columns.str.replace(" ", "_").str.lower()


# =============================================================
# 3. PASTRIMI I VLERAVE TË PRISHURA / TE PANEVOJSHME
# =============================================================
# Zëvendësojmë vlerat jo valide ("ERROR", "UNKNOWN", "", "N/A", etj.) me NaN

cols_to_clean = ["quantity", "price_per_unit", "item", "total_spent",
                 "payment_method", "location", "transaction_date"]

df_clean[cols_to_clean] = df_clean[cols_to_clean].replace(
    ["ERROR", "UNKNOWN", "", "nan", "NaN", "None", "N/A"],
    np.nan
)


# =============================================================
# 4. KORRIGJIMI I TIPOLOGJISË (DATA TYPES)
# =============================================================

# 4.1 Rregullimi i kolonave tekstuale (heq hapësirat e tepërta)
for col in ["transaction_id", "item", "payment_method", "location"]:
    df_clean[col] = df_clean[col].astype(str).str.strip()

# 4.2 Konvertimi i kolonave numerike
df_clean["quantity"] = pd.to_numeric(df_clean["quantity"], errors="coerce")
df_clean["price_per_unit"] = pd.to_numeric(df_clean["price_per_unit"], errors="coerce")
df_clean["total_spent"] = pd.to_numeric(df_clean["total_spent"], errors="coerce")

# 4.3 Konvertimi i dates
df_clean["transaction_date"] = pd.to_datetime(df_clean["transaction_date"], errors="coerce")

# Nxjerrim vitin, muajin dhe ditën e javës
df_clean["year"] = df_clean["transaction_date"].dt.year
df_clean["month"] = df_clean["transaction_date"].dt.month
df_clean["day_of_week"] = df_clean["transaction_date"].dt.dayofweek


# =============================================================
# 5. MBUSHJA E VLERAVE MUNGUAR PËR ITEM / PRICE
# =============================================================

# Çmime standarde për artikuj me mungesë të price_per_unit
price_dict = {
    'Coffee': 2.0, 'Tea': 1.5, 'Sandwich': 4.0,
    'Salad': 5.0, 'Cake': 3.0, 'Cookie': 1.0,
    'Smoothie': 4.0, 'Juice': 3.0
}

# Mbushim price_per_unit kur item dihet
df_clean["price_per_unit"] = df_clean["price_per_unit"].fillna(df_clean["item"].map(price_dict))

# Rast i kundërt: kur price-per-unit ekziston por mungon item-i
price_to_name = {
    2.0: 'Coffee',
    1.5: 'Tea',
    5.0: 'Salad',
    1.0: 'Cookie'
}

df_clean["item"] = df_clean["item"].fillna(df_clean["price_per_unit"].map(price_to_name))


# =============================================================
# 6. MBUSHJA E VLERAVE MUNGUAR DUKE PËRDORUR FORMULAT
# =============================================================
# Formula bazë:
# total_spent = quantity * price_per_unit

# 6.1 Llogarit total_spent kur mungon
mask_total = df_clean["total_spent"].isna() & df_clean["quantity"].notna() & df_clean["price_per_unit"].notna()
df_clean.loc[mask_total, "total_spent"] = (
    df_clean.loc[mask_total, "quantity"] * df_clean.loc[mask_total, "price_per_unit"]
)

# 6.2 Llogarit quantity kur mungon
mask_quantity = df_clean["quantity"].isna() & df_clean["total_spent"].notna() & df_clean["price_per_unit"].notna()
df_clean.loc[mask_quantity, "quantity"] = (
    df_clean.loc[mask_quantity, "total_spent"] / df_clean.loc[mask_quantity, "price_per_unit"]
)

# 6.3 Llogarit price_per_unit kur mungon
mask_price = df_clean["price_per_unit"].isna() & df_clean["quantity"].notna() & df_clean["total_spent"].notna()
df_clean.loc[mask_price, "price_per_unit"] = (
    df_clean.loc[mask_price, "total_spent"] / df_clean.loc[mask_price, "quantity"]
)


# =============================================================
# 7. MBUSHJA E NAN-VE TË MBETURA ME MESATARE
# =============================================================
df_clean["total_spent"] = df_clean["total_spent"].fillna(df_clean["total_spent"].mean())
df_clean["quantity"] = df_clean["quantity"].fillna(df_clean["quantity"].mean())
df_clean["price_per_unit"] = df_clean["price_per_unit"].fillna(df_clean["price_per_unit"].mean())


# =============================================================
# 8. HEQJA E RRESHTAVE PA VLERË
# =============================================================
df_clean = df_clean.dropna(subset=["transaction_date"])
df_clean = df_clean.dropna(subset=["item"])


# =============================================================
# 9. (OPSIONALE) RUAJTJA E DATASET-IT TË PASTRUAR
# =============================================================
# df_clean.to_csv("clean_cafe_sales.csv", index=False)


# =============================================================
# 10. EDA – Exploratory Data Analysis
# =============================================================
# Qëllimi: të kuptojmë datasetin me statistika, counts, dhe totalet.

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



# =============================================================
# 11. Vizualizimi
# =============================================================

# 1. Bar Chart
# A
total_sales = df_clean.groupby('item')['total_spent'].sum()

x = list(df['item'])
y = list(df['total_sales'])

plt.bar(x, y)

# B

payments = df['payment_method'].value_counts()

x2 = payments
y2 = list(df['total_sales'])

plt.bar(x2, y2)

# 2.