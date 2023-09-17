import unittest

from numpy import array

from src import Series, Tensor


class SeriesTest(unittest.TestCase):

    def test_series_poly_array(self):
        a0 = Series(array([1, 2, 7]))

        a0 = a0.evaluate(array([1]))

        a2 = array([10])
        self.assertEqual(a0, a2)

    def test_series_poly_float(self):
        a0 = Series(array([7, 21, 9]))

        a0 = a0.evaluate(2)

        a2 = 85
        self.assertEqual(a0, a2)

    def test_tensor_polys(self):
        a0 = Tensor(array([[1.0, 2.0, 7.0],
                           [1.0, 2.0, 3.0],
                           [1.0, 2.0, 7.0]]))

        a0 = a0.reduce(1)

        a2 = Series(array([10, 6, 10]))
        self.assertEqual(a0, a2)


if __name__ == '__main__':
    unittest.main()
