from __future__ import annotations
from typing import List, Union
from decimal import Decimal, getcontext

_IterativeConstant_operator_counter = 0
getcontext().prec = 1000


def set_decimal_precision(precision: int):
    getcontext().prec = precision


def get_counter() -> int:
    return _IterativeConstant_operator_counter


class Formatter:

    @staticmethod
    def _i_to_script(i: int, subscript: bool = True):
        subscripts = {
            '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄', '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉'
        }
        superscripts = {
            '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
        }
        i_string = ""
        i = str(i)
        for character in i:
            if subscript:
                i_string += subscripts[character]
            else:
                i_string += superscripts[character]
        return i_string


class ScalerHolder(Formatter):

    def __init__(self, initial_constants: List[Union[float, Decimal]], name: str):
        super().__init__()
        self.name: str = name
        self.constants: List[Decimal] = []
        for initial_constant in initial_constants:
            initial_constant = Decimal(initial_constant)
            self.constants.append(initial_constant)

    def condense(self) -> str:
        condensed_string = ""
        num_constant = len(self.constants)
        for i, value in enumerate(self.constants):
            formatted_value = "{:.3e}".format(value)
            i_string = self._i_to_script(i, subscript=False)
            condensed_string += f"{formatted_value} {self.name}{i_string}"
            if i != num_constant - 1:
                condensed_string += " + "
        return condensed_string

    def __str__(self) -> str:
        return self.condense()

    def __eq__(self, holder: ScalerHolder) -> bool:
        if isinstance(holder, ScalerHolder):
            return self.condense() == holder.condense()
        return NotImplemented

    def copy(self) -> ScalerHolder:
        return ScalerHolder(initial_constants=self.constants, name=self.name)

    def scale(self, value: Union[float, Decimal]) -> ScalerHolder:
        value = Decimal(value)
        new_constants = []
        for constant in self.constants:
            new_constants.append(value * constant)
        return ScalerHolder(initial_constants=new_constants, name=self.name)

    def increase_scaler(self) -> ScalerHolder:
        holder = self.copy()
        holder.constants.insert(0, Decimal(0))
        return holder

    def add(self, holder: ScalerHolder) -> ScalerHolder:
        if holder.name != self.name:
            raise TypeError("Scaler types do not match")

        len_self_constants = len(self.constants)
        len_holder_constants = len(holder.constants)

        new_constants = [0] * max(len_self_constants, len_holder_constants)
        for i in range(len(new_constants)):
            if i < len_self_constants:
                new_constants[i] += self.constants[i]
            if i < len_holder_constants:
                new_constants[i] += holder.constants[i]

        return ScalerHolder(initial_constants=new_constants, name=self.name)

    def multiply(self, holder: ScalerHolder) -> ScalerHolder:
        if holder.name != self.name:
            raise TypeError("Scaler types do not match")
        self_holder = self.copy()

        len_self_constants = len(self_holder.constants)
        len_holder_constants = len(holder.constants)
        max_len_constants = max(len_self_constants, len_holder_constants)

        # Pad so that both have the same size
        self_holder.constants.extend([Decimal(0)] * max(0, max_len_constants - len_self_constants))
        holder.constants.extend([Decimal(0)] * max(0, max_len_constants - len_holder_constants))

        new_constants = []
        for n in range(2 * max_len_constants - 1):
            constant = Decimal(0)
            for i in range(len_self_constants):
                if len_holder_constants > n - i >= 0:
                    constant += self_holder.constants[i] * holder.constants[n - i]
            new_constants.append(constant)

        return ScalerHolder(initial_constants=new_constants, name=self.name)


class IterativeConstant(Formatter):

    def __init__(self, initial_holders: List[ScalerHolder], name: str):
        super().__init__()
        self.name: str = name
        self.holders: List[ScalerHolder] = initial_holders

    def condense(self) -> str:
        condensed_string = "["
        num_constant = len(self.holders)
        for i, holder in enumerate(self.holders):
            holder_str = holder.condense()
            i_string = self._i_to_script(i, subscript=True)
            condensed_string += f"{self.name}{i_string}: {holder_str}"
            if i != num_constant - 1:
                condensed_string += ", "

        condensed_string += "]"
        return condensed_string

    def __str__(self) -> str:
        return self.condense()

    def __eq__(self, iterator: IterativeConstant) -> bool:
        if isinstance(iterator, IterativeConstant):
            return self.condense() == iterator.condense()
        return NotImplemented

    def copy(self) -> IterativeConstant:
        return IterativeConstant(initial_holders=self.holders, name=self.name)

    @staticmethod
    def update_counter():
        global _IterativeConstant_operator_counter
        _IterativeConstant_operator_counter += 1

    def update(self, i: int, holder: ScalerHolder) -> IterativeConstant:
        self.update_counter()

        if i > len(self.holders):
            raise ValueError(f"Update at index {i} out of range {len(self.holders)}")

        iterator = self.copy()
        if i < len(iterator.holders):
            iterator.holders[i] = holder
        elif i == len(iterator.holders):
            iterator.holders.append(holder)
        return iterator

    def get(self, i: int) -> ScalerHolder:
        return self.holders[i]
