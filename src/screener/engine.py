import sqlite3
import pandas as pd
import yaml

from pathlib import Path

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

        score_columns = [

            "return_on_equity_pct",

            "net_profit_margin_pct",

            "asset_turnover"

        ]

        self.df["composite_quality_score"] = (

            self.df[score_columns]

            .fillna(0)

            .mean(axis=1)

        )

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

    for preset in presets:

        result = engine.apply_filters(preset)

        print("\n" + "=" * 60)
        print(f"Preset : {preset}")
        print(f"Companies Found : {len(result)}")

        print(
            result[
                [
                    "company_id",
                    "year",
                    "return_on_equity_pct",
                    "debt_to_equity",
                    "composite_quality_score"
                ]
            ].head(5)
        )