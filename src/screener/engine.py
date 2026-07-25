import sqlite3
from pathlib import Path

import pandas as pd
import yaml
from export_excel import export_screeners

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "output" / "nifty100.db"
CONFIG_PATH = BASE_DIR / "config" / "screener_config.yaml"


class ScreenerEngine:

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)

        print(CONFIG_PATH)

        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        print("Configuration Loaded")

        self.df = pd.read_sql(
            "SELECT * FROM financial_ratios",
            self.conn
        )

        print(
            f"{len(self.df)} financial ratio records loaded."
        )

    def add_composite_score(self):

        df = self.df.copy()

        # ---------- Profitability ----------
        df["profitability_score"] = (
                df["return_on_equity_pct"].fillna(0) * 0.50 +
                df["net_profit_margin_pct"].fillna(0) * 0.30 +
                df["operating_profit_margin_pct"].fillna(0) * 0.20
        )

        # ---------- Cash ----------
        df["cash_score"] = (
                df["free_cash_flow_cr"].fillna(0) * 0.70 +
                df["cash_from_operations_cr"].fillna(0) * 0.30
        )

        # ---------- Leverage ----------
        df["leverage_score"] = (
                (1 / (df["debt_to_equity"].fillna(0) + 1)) * 100
        )

        # ---------- Efficiency ----------
        df["efficiency_score"] = (
                df["asset_turnover"].fillna(0) * 100
        )

        # ---------- Final Score ----------
        df["composite_quality_score"] = (

                df["profitability_score"] * 0.40 +

                df["cash_score"] * 0.25 +

                df["leverage_score"] * 0.20 +

                df["efficiency_score"] * 0.15

        )

        self.df = df

    def apply_filters(self, preset_name):

        filters = self.config["filters"][preset_name]

        df = self.df.copy()

        for key, value in filters.items():

            if key == "roe_min":
                df = df[df["return_on_equity_pct"] >= value]

            elif key == "debt_to_equity_max":
                df = df[df["debt_to_equity"] <= value]

            elif key == "free_cash_flow_min":
                df = df[df["free_cash_flow_cr"] >= value]

            elif key == "operating_profit_margin_min":
                df = df[
                    df["operating_profit_margin_pct"] >= value
                    ]

        df = df.sort_values(
            "composite_quality_score",
            ascending=False
        )

        return df

if __name__ == "__main__":

    engine = ScreenerEngine()

    engine.add_composite_score()

    presets = [

        "quality_compounder",

        "value_pick",

        "growth_accelerator",

        "dividend_champion",

        "debt_free_blue_chip",

        "turnaround_watch"

    ]

    results = {}

    for preset in presets:

        result = engine.apply_filters(preset)

        results[preset] = result

        print("\n" + "=" * 60)

        print(preset)

        print(f"Companies : {len(result)}")

    export_screeners(results)

    print("\nSprint 3 Day 17 Complete.")