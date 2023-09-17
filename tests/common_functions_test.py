import unittest
from decimal import Decimal

from src import Sin, ScalerHolder, IterativeConstant


class BaseOperators(unittest.TestCase):

    def test_sin(self):
        f_n = Sin()
        for _ in range(7):
            f_n.next_term()

        a0 = f_n.get(7)

        a2 = ScalerHolder(initial_constants=[- Decimal(1) / Decimal(5040)], name="Bo")
        self.assertEqual(a0, a2)

    def test_max_sin(self):
        f_n = Sin(max_n=5)
        for _ in range(7):
            f_n.next_term()

        a0 = f_n.get(7)

        a2 = ScalerHolder(initial_constants=[0], name="Bo")
        self.assertEqual(a0, a2)


if __name__ == '__main__':
    unittest.main()
