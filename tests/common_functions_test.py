import unittest
from decimal import Decimal
from math import pi

from src import Sin, Cos, ScalerHolder


class CommonFunctionsTests(unittest.TestCase):

    def test_sin(self):
        f_n = Sin(name="f", holder_name="Bo")
        for _ in range(9):
            f_n.next_term()

        a0 = f_n.get(9)

        a2 = ScalerHolder(initial_constants=[Decimal(1) / Decimal(362880)], name="Bo")
        self.assertEqual(a0, a2)

    def test_sin_max(self):
        f_n = Sin(name="f", holder_name="Bo", max_n=5)
        for _ in range(9):
            f_n.next_term()

        a0 = f_n.get(7)

        a2 = ScalerHolder(initial_constants=[0], name="Bo")
        self.assertEqual(a0, a2)

    def test_sin_accuracy(self):
        f_n = Sin(name="f", holder_name="Bo")
        for _ in range(27):
            f_n.next_term()

        sin_approx = f_n.freeze()
        sin_approx = sin_approx.flatten()

        a0 = sin_approx.evaluate(pi)

        self.assertEqual(round(a0, 15), 0)

    def test_cos(self):
        f_n = Cos(name="g", holder_name="Bo")
        for _ in range(8):
            f_n.next_term()

        a0 = f_n.get(8)

        a2 = ScalerHolder(initial_constants=[Decimal(1) / Decimal(40320)], name="Bo")
        self.assertEqual(a0, a2)

    def test_cos_max(self):
        f_n = Cos(name="g", holder_name="Bo", max_n=5)
        for _ in range(8):
            f_n.next_term()

        a0 = f_n.get(6)

        a2 = ScalerHolder(initial_constants=[0], name="Bo")
        self.assertEqual(a0, a2)

    def test_cos_accuracy(self):
        f_n = Cos(name="g", holder_name="Bo")
        for _ in range(26):
            f_n.next_term()

        cos_approx = f_n.freeze()
        cos_approx = cos_approx.flatten()

        a0 = cos_approx.evaluate(pi)

        self.assertEqual(round(a0, 15), -1)


if __name__ == '__main__':
    unittest.main()
