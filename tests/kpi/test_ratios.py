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

    def test_debt_to_equity(self):
        self.assertEqual(
            debt_to_equity(
                500,
                500,
                500
            ),
            0.5
        )

    def test_debt_free(self):
        self.assertEqual(
            debt_to_equity(
                0,
                100,
                100
            ),
            0
        )

    def test_high_leverage(self):
        self.assertTrue(
            high_leverage_flag(
                6,
                False
            )
        )

    def test_interest_coverage(self):
        self.assertEqual(
            interest_coverage_ratio(
                200,
                50,
                50
            ),
            5.0
        )

    def test_interest_zero(self):
        self.assertIsNone(
            interest_coverage_ratio(
                100,
                50,
                0
            )
        )

    def test_icr_label(self):
        self.assertEqual(
            icr_label(0),
            "Debt Free"
        )

    def test_net_debt(self):
        self.assertEqual(
            net_debt(
                1000,
                200
            ),
            800
        )

    def test_asset_turnover(self):
        self.assertEqual(
            asset_turnover(
                2000,
                1000
            ),
            2.0
        )


if __name__ == "__main__":
    unittest.main()