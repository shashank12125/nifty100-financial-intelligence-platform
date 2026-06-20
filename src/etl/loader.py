import pandas as pd
from pathlib import Path

from normaliser import normalize_ticker, normalize_year

RAW_PATH = Path("data/raw")
SUPPORT_PATH = Path("data/supporting")


def load_excel(file_path, header=1):
    """Load Excel file and return DataFrame"""

    try:
        df = pd.read_excel(file_path, header=header)

        # Normalize company_id if present
        if "company_id" in df.columns:
            df["company_id"] = df["company_id"].apply(normalize_ticker)

        # Normalize year if present
        if "year" in df.columns:
            df["year"] = df["year"].apply(normalize_year)

        print(f"\n{'=' * 60}")
        print(f"Loaded: {file_path.name}")
        print(f"Shape : {df.shape}")

        return df

    except Exception as e:
        print(f"Error loading {file_path.name}: {e}")
        return None


if __name__ == "__main__":

    core_files = [
        "companies.xlsx",
        "profitandloss.xlsx",
        "balancesheet.xlsx",
        "cashflow.xlsx",
        "analysis.xlsx",
        "documents.xlsx",
        "prosandcons.xlsx",
    ]

    support_files = [
        "sectors.xlsx",
        "stock_prices.xlsx",
        "market_cap.xlsx",
        "financial_ratios.xlsx",
        "peer_groups.xlsx",
    ]

    print("\nLOADING CORE DATASETS")

    for file in core_files:
        load_excel(RAW_PATH / file)

    print("\nLOADING SUPPORTING DATASETS")

    for file in support_files:
        load_excel(SUPPORT_PATH / file, header=0)

    print("\nAll datasets loaded successfully.")