import unittest

from tqdm import tqdm

from src.recursive_math import IterativeConstant, ScalerHolder, Progress


class LoadingBarTest(unittest.TestCase):

    def test_loading_bar(self):

        total = 82
        with tqdm(total=total, desc="Testing loading bar") as pbar:
            Progress.set_pbar(pbar)
            Progress.reset_counter()

            a = ScalerHolder(initial_constants=[1, 2, 3], name="Bo")
            a.scale(1)

            a0 = IterativeConstant(initial_holders=[a, a, a], name="a")
            a0.conv(a0, i=0, n=2, n_index=2)

            b = ScalerHolder(initial_constants=[1, 2, 3], name="Bo")
            b.scale(1)

            b0 = IterativeConstant(initial_holders=[a, b, a], name="a")

            a0.conv(b0, i=0, n=2, n_index=2)

            counter = Progress.get_counter()
            self.assertEqual(total, counter)

        Progress.reset_counter()
        a0.scale(2)

        counter = Progress.get_counter()
        self.assertEqual(8, counter)


if __name__ == '__main__':
    unittest.main()
