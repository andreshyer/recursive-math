from decimal import Decimal

from src.iterative_constants import IterativeConstant, ScalerHolder


def factorial(n: int) -> Decimal:
    value = Decimal(1)
    for i in range(1, n + 1):
        value *= Decimal(i)
    return value


class Sin(IterativeConstant):

    def __init__(self, name: str, holder_name: str, max_n: int = 27):
        self.max_n: int = max_n
        holder = ScalerHolder(initial_constants=[0], name=holder_name)
        super().__init__(initial_holders=[holder], name=name)

    def next_term(self) -> IterativeConstant:
        n_p_1 = len(self)
        if n_p_1 % 2 == 0 or n_p_1 > self.max_n:
            value = 0
        else:
            value = Decimal(1) / factorial(n_p_1)
            sign = float((-1) ** ((n_p_1 - 1) / 2))
            value = Decimal(sign) * value

        holder = ScalerHolder(initial_constants=[value], name=self.holders[0].name)
        return self.append(holder)


class Cos(IterativeConstant):

    def __init__(self, name: str, holder_name: str, max_n: int = 26):
        self.max_n: int = max_n
        holder = ScalerHolder(initial_constants=[1], name=holder_name)
        super().__init__(initial_holders=[holder], name=name)

    def next_term(self) -> IterativeConstant:
        n_p_1 = len(self)
        if n_p_1 % 2 != 0 or n_p_1 > self.max_n:
            value = 0
        else:
            value = Decimal(1) / factorial(n_p_1)
            sign = float((-1) ** (n_p_1 / 2))
            value = Decimal(sign) * value

        holder = ScalerHolder(initial_constants=[value], name=self.holders[0].name)
        return self.append(holder)
