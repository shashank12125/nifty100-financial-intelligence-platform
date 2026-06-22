import pandas as pd

companies = pd.read_excel(
    "data/raw/companies.xlsx",
    header=1
)

companies["id"] = (
    companies["id"]
    .astype(str)
    .str.strip()
    .str.upper()
)

print(sorted(companies["id"].tolist()))