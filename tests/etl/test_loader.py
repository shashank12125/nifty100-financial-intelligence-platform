import unittest
from pathlib import Path
from unittest.mock import patch

import pandas as pd

from src.etl.loader import load_excel


class TestLoader(unittest.TestCase):

    @patch("src.etl.loader.pd.read_excel")
    def test_load_excel(self, mock_read):

        mock_read.return_value = pd.DataFrame({
            "company_id": [" abb "],
            "year": ["Mar 2024"]
        })

        df = load_excel(Path("dummy.xlsx"))

        self.assertEqual(df.shape[0], 1)
        self.assertEqual(df["company_id"][0], "ABB")
        self.assertEqual(df["year"][0], "2024-03")


if __name__ == "__main__":
    unittest.main()