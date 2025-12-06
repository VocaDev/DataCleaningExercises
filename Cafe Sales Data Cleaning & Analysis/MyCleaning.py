import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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
# 11. Vizualizimi – Shpjegime dhe Grafika
# =============================================================

# 1. Bar Charts
# -----------------
# A. Shitjet totale për secilin artikull
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
# B. Numri i pagesave sipas metodës së pagesës
"""
payments = df_clean["payment_method"].value_counts()

x = list(payments.index)
y = list(payments.values)

plt.figure(figsize=(8,5))

# Ngjyra të personalizuara për çdo metodë pagese
colors = ["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#CCB974"]

bars = plt.bar(x, y, color=colors[:len(x)], width=0.55, edgecolor="black", linewidth=1.2)

# Titulli dhe etiketat
plt.title("Count of Payment Methods", fontsize=16, fontweight="bold", pad=15)
plt.xlabel("Payment Method", fontsize=13)
plt.ylabel("Count", fontsize=13)

# Grid horizontal për referencë vizuale
plt.grid(axis="y", linestyle="--", alpha=0.4)

# Vendos etiketa mbi çdo shtyllë për lexueshmëri
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
"""

# 2. Line Chart – Shitjet me kalimin e kohës
"""
# Grupimi sipas vitit dhe muajit dhe marrja e totalit
monthly_spent = df_clean.groupby(['year', 'month'])['total_spent'].sum().reset_index()

# Krijo kolonën 'date' për timeline
monthly_spent['date'] = pd.to_datetime(monthly_spent[['year', 'month']].assign(day=1))

# Rendit sipas date
monthly_spent = monthly_spent.sort_values('date')

# Vizualizimi
plt.figure(figsize=(10,5))
plt.plot(monthly_spent['date'], monthly_spent['total_spent'], marker='o', color="#4C72B0")
plt.title("Shitjet me kalimin e kohës", fontsize=16, fontweight="bold")
plt.xlabel("Data", fontsize=13)
plt.ylabel("Shpenzimet", fontsize=13)
plt.xticks(rotation=45)
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()
"""

# 3. Pie Chart – Përqindja e mënyrave të pagesës
"""
paymet_count = df_clean["payment_method"].value_counts()

values = paymet_count.values
labels = paymet_count.index

plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, explode=[0.1, 0, 0], shadow=True,
        colors=["#4C72B0", "#55A868", "#CF282E"])
plt.title("Përqindja e mënyrave të pagesës", fontsize=16, fontweight="bold")
plt.axis('equal')  # për të bërë rrethin perfekt
plt.show()
"""

# 4. Histogram – Shpërndarja e sasisë dhe e shpenzimeve
"""
# A. Quantity
data = df_clean["quantity"]

plt.figure(figsize=(8,5))
plt.hist(data, bins=10, color="#4C72B0", edgecolor="black", alpha=0.7)
plt.title("Shpërndarja e Sasisë së Artikujve", fontsize=16, fontweight="bold")
plt.xlabel("Sasia", fontsize=13)
plt.ylabel("Numri i Transaksioneve", fontsize=13)
plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.show()

# B. Total Spent
data = df_clean["total_spent"]

plt.figure(figsize=(8,5))
sns.histplot(data, bins=10, kde=True, color="#4FB63D", edgecolor="black", alpha=0.7)
plt.title("Shpërndarja e Shpenzimeve Totale", fontsize=16, fontweight="bold")
plt.xlabel("Shpenzimet", fontsize=13)
plt.ylabel("Numri i Transaksioneve", fontsize=13)
plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.show()
"""

# 5. BoxPlot – Krahasimi i çmimeve mes artikujve
"""
plt.figure(figsize=(10,6))
sns.boxplot(
    x="item",
    y="price_per_unit",
    data=df_clean,
    palette="Set2"  # ngjyra të ndryshme për artikujt
)
plt.title("Krahasimi i Çmimeve për Artikuj", fontsize=16, fontweight="bold")
plt.xlabel("Artikulli", fontsize=13)
plt.ylabel("Çmimi për Njësi (€)", fontsize=13)
plt.xticks(rotation=45, ha='right')  # për të lexuar emrat e artikujve
plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.show()
"""

# 6. HeatMap – Korelacionet e kolonave numerike
"""
df_numeric = df_clean.select_dtypes(include=np.number)
df_corr = df_numeric.corr()

plt.figure(figsize=(8,6))
sns.heatmap(
    df_corr, 
    annot=True,        # tregon vlerat e korelacionit mbi çdo qelizë
    fmt=".2f",         # 2 shifra pas presjes dhjetore
    cmap="coolwarm",   # gradient ngjyrash (kuq-blue)
    linewidths=0.5,    # linja midis qelizave
    square=True
)
plt.title("Heatmap – Korelacionet e kolonave numerike", fontsize=16, fontweight="bold")
plt.tight_layout()
plt.show()
"""

# =============================================================
# Përfundim
# =============================================================
# ✅ Deri këtu kemi: 
# 1. Pastruar të dhënat (kolonat numerike dhe tekstuale, NaN, outlier)
# 2. Analizuar datasetin me statistika bazë dhe grupime
# 3. Vizualizuar me: bar chart, line chart, pie chart, histogram, boxplot dhe heatmap
# Kjo përbën një workflow të plotë nga "dirty file" tek "clean & analyzed dataset".
