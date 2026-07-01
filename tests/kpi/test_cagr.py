import unittest

from src.analytics.cagr import *


class TestCAGR(unittest.TestCase):

    def test_normal(self):

        value, flag = calculate_cagr(
            100,
            200,
            5
        )

        self.assertIsNone(flag)
        self.assertAlmostEqual(
            value,
            14.87,
            places=2
        )

    def test_decline_to_loss(self):

        value, flag = calculate_cagr(
            100,
            -50,
            5
        )

        self.assertEqual(
            flag,
            "DECLINE_TO_LOSS"
        )

    def test_turnaround(self):

        value, flag = calculate_cagr(
            -100,
            100,
            5
        )

        self.assertEqual(
            flag,
            "TURNAROUND"
        )

    def test_both_negative(self):

        value, flag = calculate_cagr(
            -100,
            -50,
            5
        )

        self.assertEqual(
            flag,
            "BOTH_NEGATIVE"
        )

    def test_zero_base(self):

        value, flag = calculate_cagr(
            0,
            100,
            5
        )

        self.assertEqual(
            flag,
            "ZERO_BASE"
        )

    def test_invalid_period(self):

        value, flag = calculate_cagr(
            100,
            200,
            0
        )

        self.assertEqual(
            flag,
            "INVALID_PERIOD"
        )

    def test_revenue(self):

        value, flag = revenue_cagr(
            100,
            150,
            5
        )

        self.assertIsNone(flag)

    def test_pat(self):

        value, flag = pat_cagr(
            100,
            180,
            5
        )

        self.assertIsNone(flag)

    def test_eps(self):

        value, flag = eps_cagr(
            10,
            20,
            5
        )

        self.assertIsNone(flag)

    def test_insufficient(self):

        value, flag = insufficient_data()

        self.assertEqual(
            flag,
            "INSUFFICIENT"
        )


if __name__ == "__main__":
    unittest.main()