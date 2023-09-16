import unittest
from decimal import Decimal
from src import IterativeConstant, ScalerHolder


class BaseOperators(unittest.TestCase):

    def test_scaler_add(self):
        a0 = ScalerHolder(initial_constants=[1], name="Bo")
        a1 = ScalerHolder(initial_constants=[3], name="Bo")

        a0 = a0.add(a1)

        a2 = ScalerHolder(initial_constants=[4], name="Bo")
        self.assertEqual(a0, a2)

    def test_scaler_increase_order(self):
        a0 = ScalerHolder(initial_constants=[1], name="Bo")
        a1 = ScalerHolder(initial_constants=[3], name="Bo")

        a0 = a0.increase_scaler()
        a0 = a0.increase_scaler()
        a0 = a0.add(a1)

        a2 = ScalerHolder(initial_constants=[3, 0, 1], name="Bo")
        self.assertEqual(a0, a2)

    def test_scaler_decimal_add(self):
        a0 = ScalerHolder(initial_constants=[Decimal(1)], name="Bo")
        a1 = ScalerHolder(initial_constants=[3.0], name="Bo")

        a0 = a0.add(a1)

        a2 = ScalerHolder(initial_constants=[Decimal(4)], name="Bo")
        self.assertEqual(a0, a2)

    def test_scaler_multiply(self):
        a0 = ScalerHolder(initial_constants=[1, 2, 3], name="Bo")
        a1 = ScalerHolder(initial_constants=[1, 2, 3], name="Bo")

        a0 = a0.multiply(a1)

        a2 = ScalerHolder(initial_constants=[1, 4, 10, 12, 9], name="Bo")
        self.assertEqual(a0, a2)

    def test_scaler_scale(self):
        a0 = ScalerHolder(initial_constants=[1, 2, 3], name="Bo")

        a0 = a0.scale(-1)

        a2 = ScalerHolder(initial_constants=[-1, -2, -3], name="Bo")
        self.assertEqual(a0, a2)

    def test_scalar_copy(self):
        a0 = ScalerHolder(initial_constants=[1, 2, 3], name="Bo")
        a1 = a0.copy()

        a0 = a0.add(a1)

        a2 = ScalerHolder(initial_constants=[2, 4, 6], name="Bo")
        self.assertEqual(a0, a2)

    def test_scaler_immutability(self):
        a0 = ScalerHolder(initial_constants=[1, -2, 3], name="Bo")

        a0.add(a0.copy())
        a0.multiply(a0.copy())
        a0.increase_scaler()

        a2 = ScalerHolder(initial_constants=[1, -2, 3], name="Bo")
        self.assertEqual(a0, a2)

    def test_scaler_slice(self):
        a0 = ScalerHolder(initial_constants=[1, 2, 3], name="Bo")
        a2 = ScalerHolder(initial_constants=[1], name="Bo")

        a0 = a0[:1]

        self.assertEqual(a0, a2)

    def test_iterator_get(self):
        a = ScalerHolder(initial_constants=[1], name="Bo")
        b_n = IterativeConstant(initial_holders=[a], name="a")
        self.assertEqual(a, b_n.get(0))

    def test_iterator_copy(self):
        a = ScalerHolder(initial_constants=[1], name="Bo")
        b_n = IterativeConstant(initial_holders=[a, a.add(a.copy())], name="a")

        a0 = b_n.copy().get(1)
        a2 = ScalerHolder(initial_constants=[2], name="Bo")
        self.assertEqual(a0, a2)

    def test_iterator_append(self):
        a = ScalerHolder(initial_constants=[1, 2, 3], name="Bo")
        b_n = IterativeConstant(initial_holders=[a], name="a")

        b_n.append(a.add(a.copy()))
        a0 = b_n.get(1)

        a2 = ScalerHolder(initial_constants=[2, 4, 6], name="Bo")
        self.assertTrue(len(b_n.holders) == 2)
        self.assertEqual(a0, a2)

    def test_iterator_update(self):
        a = ScalerHolder(initial_constants=[1, 2, 3], name="Bo")
        b_n = IterativeConstant(initial_holders=[a], name="a")

        b_n.update(0, a.add(a.copy()))
        a0 = b_n.get(0)

        a2 = ScalerHolder(initial_constants=[2, 4, 6], name="Bo")
        self.assertTrue(len(b_n.holders) == 1)
        self.assertEqual(a0, a2)

    def test_iterator_simple_conv(self):
        a = ScalerHolder(initial_constants=[1, 2, 3], name="Bo")
        a_n = IterativeConstant(initial_holders=[a], name="a")

        a0 = a_n.conv(a_n.copy(), i=0, n=0)

        a2 = ScalerHolder(initial_constants=[1, 4, 10, 12, 9], name="Bo")
        self.assertEqual(a0, a2)

    def test_complex_conv(self):
        a = ScalerHolder(initial_constants=[1, -2, 3], name="Bo")
        a_n = IterativeConstant(initial_holders=[a, a, a], name="a")

        a0 = a_n.conv(a_n.copy(), i=0, n=2)

        a2 = ScalerHolder(initial_constants=[3, -12, 30, -36, 27], name="Bo")
        self.assertEqual(a0, a2)


if __name__ == '__main__':
    unittest.main()
