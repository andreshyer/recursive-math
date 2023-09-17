from decimal import Decimal

from src.utils.iterative_constants import IterativeConstant, ScalerHolder


def factorial(n: int) -> Decimal:
    value = Decimal(1)
    for i in range(1, n + 1):
        value *= Decimal(i)
    return value


class Sin(IterativeConstant):

    def __init__(self, max_n: int = 100):
        self.max_n: int = max_n
        holder = ScalerHolder(initial_constants=[0], name="Bo")
        super().__init__(initial_holders=[holder], name="f")

    def next_term(self) -> IterativeConstant:
        n_p_1 = len(self)
        if n_p_1 % 2 == 0 or n_p_1 > self.max_n:
            value = 0
        else:
            value = Decimal(1) / factorial(n_p_1)
            sign = float((-1) ** ((n_p_1 - 1) / 2))
            value = Decimal(sign) * value

        holder = ScalerHolder(initial_constants=[value], name="Bo")
        return self.append(holder)

