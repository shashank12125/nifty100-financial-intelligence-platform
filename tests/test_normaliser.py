import unittest

from src.etl.normaliser import normalize_ticker, normalize_year


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


if __name__ == "__main__":
    unittest.main()