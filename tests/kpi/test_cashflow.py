import unittest

from src.analytics.cashflow_kpis import *


class TestCashFlow(unittest.TestCase):

    def test_fcf(self):

        self.assertEqual(
            free_cash_flow(
                500,
                -100
            ),
            400
        )

    def test_quality_high(self):

        self.assertEqual(
            cfo_quality_score(
                200,
                100
            ),
            "High Quality"
        )

    def test_quality_moderate(self):

        self.assertEqual(
            cfo_quality_score(
                60,
                100
            ),
            "Moderate"
        )

    def test_quality_low(self):

        self.assertEqual(
            cfo_quality_score(
                20,
                100
            ),
            "Accrual Risk"
        )

    def test_capex_light(self):

        self.assertEqual(
            capex_intensity(
                -20,
                1000
            ),
            "Asset Light"
        )

    def test_capex_heavy(self):

        self.assertEqual(
            capex_intensity(
                -150,
                1000
            ),
            "Capital Intensive"
        )

    def test_fcf_conversion(self):

        self.assertEqual(
            fcf_conversion_rate(
                200,
                400
            ),
            50
        )

    def test_pattern(self):

        self.assertEqual(
            capital_allocation_pattern(
                100,
                -50,
                -20,
                "High Quality"
            ),
            "Shareholder Returns"
        )


if __name__ == "__main__":
    unittest.main()