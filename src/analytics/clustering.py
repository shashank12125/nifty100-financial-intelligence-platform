import sqlite3

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

DB_PATH = "output/nifty100.db"

conn = sqlite3.connect(DB_PATH)

print("Connected to SQLite")

# ----------------------------
# Load Tables
# ----------------------------

companies = pd.read_sql("""
SELECT
    c.id,
    c.company_name,
    s.broad_sector
FROM companies c
LEFT JOIN sectors s
ON c.id = s.company_id
""", conn)

ratios = pd.read_sql("""
SELECT
    company_id,
    year,
    return_on_equity_pct,
    debt_to_equity,
    operating_profit_margin_pct
FROM financial_ratios
""", conn)

analysis = pd.read_sql("""
SELECT
    company_id,
    compounded_sales_growth,
    compounded_profit_growth
FROM analysis
""", conn)

# ---------------------------------
# Keep only TTM rows
# ---------------------------------

analysis = analysis[
    analysis["compounded_sales_growth"]
    .str.contains("TTM", na=False)
].copy()

# ---------------------------------
# Extract numeric percentage
# ---------------------------------

for col in [
    "compounded_sales_growth",
    "compounded_profit_growth"
]:

    analysis[col] = (
        analysis[col]
        .str.extract(r'(-?\d+)%')[0]
        .astype(float)
    )

# ----------------------------
# Latest Ratios
# ----------------------------

ratios = (
    ratios
    .sort_values("year", ascending=False)
    .drop_duplicates("company_id")
)

# ----------------------------
# Merge
# ----------------------------

df = (
    companies
    .merge(ratios, left_on="id", right_on="company_id")
    .merge(analysis, on="company_id", how="left")
)

print(f"Companies Loaded : {len(df)}")

# ----------------------------
# Features
# ----------------------------

features = [
    "return_on_equity_pct",
    "debt_to_equity",
    "operating_profit_margin_pct",
    "compounded_sales_growth",
    "compounded_profit_growth",
]

# ----------------------------
# Missing Value Imputation
# ----------------------------

for col in features:

    sector_median = df.groupby("broad_sector")[col].transform("median")

    df[col] = df[col].fillna(sector_median)

    df[col] = df[col].fillna(df[col].median())

print("Missing values handled.")

# ----------------------------
# Standard Scaling
# ----------------------------

scaler = StandardScaler()

X = scaler.fit_transform(df[features])

print("Scaling completed.")

# ----------------------------
# Elbow Plot
# ----------------------------

inertia = []

for k in range(2, 11):

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    model.fit(X)

    inertia.append(model.inertia_)

plt.figure(figsize=(8,5))

plt.plot(
    range(2,11),
    inertia,
    marker="o"
)

plt.title("KMeans Elbow Curve")
plt.xlabel("Number of Clusters")
plt.ylabel("Inertia")

plt.grid(True)

plt.tight_layout()

plt.savefig("reports/elbow_plot.png")

print("Elbow plot saved.")

# ----------------------------
# Final KMeans
# ----------------------------

kmeans = KMeans(
    n_clusters=5,
    random_state=42,
    n_init=10
)

df["cluster_id"] = kmeans.fit_predict(X)

# ----------------------------
# Distance From Centroid
# ----------------------------

distances = kmeans.transform(X)

df["distance_from_centroid"] = [

    distances[i][cluster]

    for i, cluster in enumerate(df["cluster_id"])

]

# ----------------------------
# Cluster Names
# ----------------------------

cluster_names = {

    0: "High Quality",

    1: "Growth",

    2: "Value",

    3: "Defensive",

    4: "Turnaround"

}

df["cluster_name"] = df["cluster_id"].map(cluster_names)

# ----------------------------
# Export CSV
# ----------------------------

output = df[
    [
        "id",
        "company_name",
        "cluster_id",
        "cluster_name",
        "distance_from_centroid"
    ]
].rename(columns={"id": "company_id"})

output.to_csv(

    "output/cluster_labels.csv",

    index=False

)

print()

print(output.head())

print()

print("Cluster labels saved.")

conn.close()

print("Done.")