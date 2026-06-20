import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw")
OUTPUT_PATH = Path("output")

OUTPUT_PATH.mkdir(exist_ok=True)

def dq01_pk_uniqueness(df, table_name, pk_column):
    failures = df[df.duplicated(subset=[pk_column], keep=False)]

    if not failures.empty:
        failures = failures.copy()
        failures["table_name"] = table_name
        failures["dq_rule"] = "DQ-01"
        failures["severity"] = "CRITICAL"

    return failures


def dq02_company_year_uniqueness(df, table_name):
    failures = df[df.duplicated(
        subset=["company_id", "year"],
        keep=False
    )]

    if not failures.empty:
        failures = failures.copy()
        failures["table_name"] = table_name
        failures["dq_rule"] = "DQ-02"
        failures["severity"] = "CRITICAL"

    return failures


def dq03_fk_integrity(child_df, parent_df, fk_column, pk_column, table_name):
    failures = child_df[
        ~child_df[fk_column].isin(parent_df[pk_column])
    ]

    if not failures.empty:
        failures = failures.copy()
        failures["table_name"] = table_name
        failures["dq_rule"] = "DQ-03"
        failures["severity"] = "CRITICAL"

    return failures


def dq04_balance_sheet_check(df):
    liabilities_calc = (
        df["equity_capital"].fillna(0)
        + df["reserves"].fillna(0)
        + df["borrowings"].fillna(0)
        + df["other_liabilities"].fillna(0)
    )

    assets_calc = (
        df["fixed_assets"].fillna(0)
        + df["cwip"].fillna(0)
        + df["investments"].fillna(0)
        + df["other_asset"].fillna(0)
    )

    failures = df[
        (
            abs(liabilities_calc - df["total_liabilities"])
            > (df["total_liabilities"] * 0.01)
        )
        |
        (
            abs(assets_calc - df["total_assets"])
            > (df["total_assets"] * 0.01)
        )
    ].copy()

    if not failures.empty:
        failures["table_name"] = "balancesheet"
        failures["dq_rule"] = "DQ-04"
        failures["severity"] = "WARNING"

    return failures

def dq05_opm_cross_check(df):

    calc_opm = (
        df["operating_profit"] /
        df["sales"]
    ) * 100

    failures = df[
        abs(calc_opm - df["opm_percentage"]) > 1
    ].copy()

    if not failures.empty:
        failures["table_name"] = "profitandloss"
        failures["dq_rule"] = "DQ-05"
        failures["severity"] = "WARNING"

    return failures

def dq06_positive_sales(df):

    failures = df[
        df["sales"] <= 0
    ].copy()

    if not failures.empty:
        failures["table_name"] = "profitandloss"
        failures["dq_rule"] = "DQ-06"
        failures["severity"] = "CRITICAL"

    return failures


def main():
    validation_failures = []

    print("\nRunning Data Quality Checks...\n")

    companies = pd.read_excel(
        RAW_PATH / "companies.xlsx",
        header=1
    )

    pnl = pd.read_excel(
        RAW_PATH / "profitandloss.xlsx",
        header=1
    )

    balancesheet = pd.read_excel(
        RAW_PATH / "balancesheet.xlsx",
        header=1
    )

    companies["id"] = (
        companies["id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    pnl["company_id"] = (
        pnl["company_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    failures = dq01_pk_uniqueness(
        companies,
        "companies",
        "id"
    )

    if not failures.empty:
        validation_failures.append(failures)

    failures = dq02_company_year_uniqueness(
        pnl,
        "profitandloss"
    )

    if not failures.empty:
        validation_failures.append(failures)

    failures = dq03_fk_integrity(
        pnl,
        companies,
        "company_id",
        "id",
        "profitandloss"
    )

    if not failures.empty:
        validation_failures.append(failures)

        print("\nMissing Company IDs:")
        print(sorted(set(failures["company_id"])))

    failures = dq04_balance_sheet_check(
        balancesheet
    )

    # DQ-05

    failures = dq05_opm_cross_check(pnl)

    if not failures.empty:
        validation_failures.append(failures)

    # DQ-06

    failures = dq06_positive_sales(pnl)

    if not failures.empty:
        validation_failures.append(failures)

    if validation_failures:
        result = pd.concat(
            validation_failures,
            ignore_index=True
        )

        result.to_csv(
            OUTPUT_PATH / "validation_failures.csv",
            index=False
        )

        print(
            f"\nValidation failures found: {len(result)}"
        )

        print("\nSummary:")
        print(
            result[
                ["table_name", "dq_rule"]
            ].value_counts()
        )

    else:
        print("\nAll validations passed.")


if __name__ == "__main__":
    main()