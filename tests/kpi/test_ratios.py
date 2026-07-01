import unittest

from src.analytics.ratios import *


class TestRatios(unittest.TestCase):

    def test_npm(self):
        self.assertEqual(
            net_profit_margin(100, 1000),
            10.0
        )

    def test_npm_zero_sales(self):
        self.assertIsNone(
            net_profit_margin(100, 0)
        )

    def test_opm(self):
        self.assertEqual(
            operating_profit_margin(200, 1000),
            20.0
        )

    def test_opm_check(self):
        self.assertTrue(
            check_opm(25, 23)
        )

    def test_roe(self):
        self.assertEqual(
            return_on_equity(
                100,
                500,
                500
            ),
            10.0
        )

    def test_roe_negative(self):
        self.assertIsNone(
            return_on_equity(
                100,
                -100,
                50
            )
        )

    def test_roce(self):
        self.assertEqual(
            return_on_capital_employed(
                200,
                500,
                500,
                1000
            ),
            10.0
        )

    def test_roa(self):
        self.assertEqual(
            return_on_assets(
                100,
                2000
            ),
            5.0
        )


if __name__ == "__main__":
    unittest.main()