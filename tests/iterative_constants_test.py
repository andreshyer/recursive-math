import unittest
from decimal import Decimal
from src import IterativeConstant, ScalerHolder, get_counter


class BaseOperators(unittest.TestCase):

    def test_scaler_add(self):
        a0 = ScalerHolder(initial_constants=[1], name="a")
        a1 = ScalerHolder(initial_constants=[3], name="a")

        a0 = a0.add(a1)

        a2 = ScalerHolder(initial_constants=[4], name="a")
        self.assertEqual(a0, a2)

    def test_scaler_increase_order(self):
        a0 = ScalerHolder(initial_constants=[1], name="a")
        a1 = ScalerHolder(initial_constants=[3], name="a")

        a0 = a0.increase_scaler()
        a0 = a0.increase_scaler()
        a0 = a0.add(a1)

        a2 = ScalerHolder(initial_constants=[3, 0, 1], name="a")
        self.assertEqual(a0, a2)

    def test_scaler_decimal_add(self):
        a0 = ScalerHolder(initial_constants=[Decimal(1)], name="a")
        a1 = ScalerHolder(initial_constants=[3.0], name="a")

        a0 = a0.add(a1)

        a2 = ScalerHolder(initial_constants=[Decimal(4)], name="a")
        self.assertEqual(a0, a2)

    def test_scaler_multiply(self):
        a0 = ScalerHolder(initial_constants=[1, 2, 3], name="a")
        a1 = ScalerHolder(initial_constants=[1, 2, 3], name="a")

        a0 = a0.multiply(a1)

        a2 = ScalerHolder(initial_constants=[1, 4, 10, 12, 9], name="a")
        self.assertEqual(a0, a2)

    def test_scaler_scale(self):
        a0 = ScalerHolder(initial_constants=[1, 2, 3], name="a")

        a0 = a0.scale(-1)

        a2 = ScalerHolder(initial_constants=[-1, -2, -3], name="a")
        self.assertEqual(a0, a2)

    def test_scalar_copy(self):
        a0 = ScalerHolder(initial_constants=[1, 2, 3], name="a")
        a1 = a0.copy()

        a0 = a0.add(a1)

        a2 = ScalerHolder(initial_constants=[2, 4, 6], name="a")
        self.assertEqual(a0, a2)

    def test_scaler_immutability(self):
        a0 = ScalerHolder(initial_constants=[1, -2, 3], name="a")

        a0.add(a0.copy())
        a0.multiply(a0.copy())
        a0.increase_scaler()

        a2 = ScalerHolder(initial_constants=[1, -2, 3], name="a")
        self.assertEqual(a0, a2)

    def test_iterator_get(self):
        a = ScalerHolder(initial_constants=[1], name="a")
        b_n = IterativeConstant(initial_holders=[a], name="b")
        self.assertEqual(a, b_n.get(0))

    def test_iterator_copy(self):
        a = ScalerHolder(initial_constants=[1], name="a")
        b_n = IterativeConstant(initial_holders=[a, a.add(a.copy())], name="b")

        a0 = b_n.copy().get(1)
        a2 = ScalerHolder(initial_constants=[2], name="a")
        self.assertEqual(a0, a2)

    def test_iterator_append(self):
        a = ScalerHolder(initial_constants=[1, 2, 3], name="a")
        b_n = IterativeConstant(initial_holders=[a], name="b")

        b_n.update(1, a.add(a.copy()))
        a0 = b_n.get(1)

        a2 = ScalerHolder(initial_constants=[2, 4, 6], name="a")
        self.assertTrue(len(b_n.holders) == 2)
        self.assertEqual(a0, a2)

    def test_iterator_swap(self):
        a = ScalerHolder(initial_constants=[1, 2, 3], name="a")
        b_n = IterativeConstant(initial_holders=[a], name="b")

        b_n.update(0, a.add(a.copy()))
        a0 = b_n.get(0)

        a2 = ScalerHolder(initial_constants=[2, 4, 6], name="a")
        self.assertTrue(len(b_n.holders) == 1)
        self.assertEqual(a0, a2)

    def test_counter(self):
        self.assertEqual(get_counter(), 0)

        a = ScalerHolder(initial_constants=[1, 2, 3], name="a")
        b_n = IterativeConstant(initial_holders=[a], name="b")
        c_n = IterativeConstant(initial_holders=[a], name="b")

        b_n.update(0, a.add(a.copy()))
        c_n.update(1, a.add(a.copy()))

        self.assertEqual(get_counter(), 2)


if __name__ == '__main__':
    unittest.main()
