import unittest

from src.etl.normaliser import normalize_ticker, normalize_year
import pytest
from src.etl.normaliser import normalize_year


class TestNormaliser(unittest.TestCase):

    def test_normalize_ticker(self):
        self.assertEqual(normalize_ticker(" abb "), "ABB")
        self.assertEqual(normalize_ticker("adanient"), "ADANIENT")

    def test_normalize_year(self):
        self.assertEqual(normalize_year("Mar 2014"), "2014-03")
        self.assertEqual(normalize_year("Dec 2012"), "2012-12")
        self.assertEqual(normalize_year("Mar-24"), "2024-03")
        self.assertEqual(normalize_year("FY24"), "2024-03")
        self.assertEqual(normalize_year("2023"), "2023-03")

    def test_normalize_year_mar24(self):
        self.assertEqual(normalize_year("Mar-24"), "2024-03")

    def test_normalize_year_dec24(self):
        self.assertEqual(normalize_year("Dec-24"), "2024-12")

    def test_normalize_year_fy20(self):
        self.assertEqual(normalize_year("FY20"), "2020-03")

    def test_normalize_year_none(self):
        self.assertIsNone(normalize_year(None))

    def test_normalize_year_invalid(self):
        self.assertEqual(normalize_year("Hello"), "Hello")

    def test_normalize_year_empty(self):
        self.assertEqual(normalize_year(""), "")

    def test_normalize_year_spaces(self):
        self.assertEqual(normalize_year("   "), "")

    def test_normalize_year_lowercase(self):
        self.assertEqual(normalize_year("mar 2014"), "2014-03")

    def test_normalize_year_mixedcase(self):
        self.assertEqual(normalize_year("mAr 2014"), "2014-03")

    def test_normalize_year_invalid_month(self):
        self.assertEqual(normalize_year("Jan 2024"), "Jan 2024")

    def test_normalize_year_invalid_fy(self):
        self.assertEqual(normalize_year("FY"), "FY")

    def test_normalize_year_short(self):
        self.assertEqual(normalize_year("24"), "24")

    def test_normalize_year_existing_format(self):
        self.assertEqual(normalize_year("2024-03"), "2024-03")

    def test_normalize_year_dec_lower(self):
        self.assertEqual(normalize_year("dec-23"), "2023-12")

    def test_normalize_ticker_none(self):
        self.assertIsNone(normalize_ticker(None))

    def test_normalize_ticker_spaces(self):
        self.assertEqual(normalize_ticker(" tcs "), "TCS")


if __name__ == "__main__":
    unittest.main()