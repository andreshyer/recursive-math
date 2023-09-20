from __future__ import annotations
from typing import List, Union
from decimal import Decimal, getcontext

from numpy import array

from .progress import Progress
from .series import Series, Tensor

getcontext().prec = 1000


def set_decimal_precision(precision: int):
    getcontext().prec = precision


class Formatter:

    @staticmethod
    def _i_to_script(i: int, subscript: bool = True) -> str:
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

    @staticmethod
    def check_slice(item: slice):
        if not isinstance(item, slice):
            raise IndexError("Cannot take integer slice, use .get() instead.")
        if item.start is not None:
            raise IndexError("Start cannot be defined for slice.")
        if item.step is not None:
            raise IndexError("Step cannot be defined for slice.")


class ScalerHolder(Formatter):

    def __init__(self, initial_constants: List[Union[float, Decimal]], name: str):
        super().__init__()
        self.epsilon = Decimal(10) ** (-Decimal(getcontext().prec))
        self.name: str = name
        self.constants: List[Decimal] = []
        for initial_constant in initial_constants:
            initial_constant = Decimal(initial_constant)
            self.constants.append(initial_constant)
        Progress.update()

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

    def __getitem__(self, item: slice) -> ScalerHolder:
        self.check_slice(item)

        new_constants = self.constants[item]
        return ScalerHolder(initial_constants=new_constants, name=self.name)

    def __len__(self):
        return len(self.constants)

    def get(self, i: int) -> Decimal:
        Progress.update()
        return self.constants[i]

    def copy(self) -> ScalerHolder:
        new_constants = []
        for constant in self.constants:
            new_constants.append(Decimal(constant))

        Progress.update()
        return ScalerHolder(initial_constants=self.constants.copy(), name=self.name)

    def freeze(self) -> Series:
        constants = []
        for constant in self.constants:
            constants.append(float(constant))

        Progress.update()
        return Series(array(constants))

    def scale(self, value: Union[float, Decimal]) -> ScalerHolder:
        value = Decimal(value)
        new_constants = []
        for constant in self.constants:
            new_constants.append(value * constant)

        Progress.update()
        return ScalerHolder(initial_constants=new_constants, name=self.name)

    def increase_scaler(self) -> ScalerHolder:
        holder = self.copy()
        holder.constants.insert(0, Decimal(0))

        Progress.update()
        return holder

    def add(self, holder: ScalerHolder) -> ScalerHolder:
        if holder.name != self.name:
            raise TypeError("Scaler types do not match")

        len_self_constants = len(self.constants)
        len_holder_constants = len(holder.constants)

        new_constants = [Decimal(0)] * max(len_self_constants, len_holder_constants)
        for i in range(len(new_constants)):
            if i < len_self_constants:
                new_constants[i] += self.constants[i]
            if i < len_holder_constants:
                new_constants[i] += holder.constants[i]

        Progress.update()
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

        upper_index = len(new_constants) - 1
        while upper_index >= 0 and new_constants[upper_index] <= self.epsilon:
            upper_index -= 1
        new_constants = new_constants[:upper_index + 1]

        Progress.update()
        return ScalerHolder(initial_constants=new_constants, name=self.name)


class IterativeConstant(Formatter):

    def __init__(self, initial_holders: List[ScalerHolder], name: str):
        super().__init__()
        self.holders: List[ScalerHolder] = initial_holders
        self.name = name
        self.verify_names(self)
        Progress.update()

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

    @staticmethod
    def verify_names(iterator: IterativeConstant):
        names = []
        for holder in iterator.holders:
            names.append(holder.name)

        if len(names) > 1:
            base_name = names[0]
            for name in names:
                if name != base_name:
                    raise ValueError("Names do not match in holders.")

    def __str__(self) -> str:
        return self.condense()

    def __eq__(self, iterator: IterativeConstant) -> bool:
        if isinstance(iterator, IterativeConstant):
            return self.condense() == iterator.condense()
        return NotImplemented

    def __getitem__(self, item: slice) -> IterativeConstant:
        self.check_slice(item)

        new_holders = self.holders[item]
        return IterativeConstant(initial_holders=new_holders, name=self.name)

    def __len__(self):
        return len(self.holders)

    def get(self, i: int) -> ScalerHolder:
        Progress.update()
        return self.holders[i]

    def copy(self) -> IterativeConstant:
        new_holders = []
        for holder in self.holders:
            new_holders.append(holder.copy())

        Progress.update()
        return IterativeConstant(initial_holders=new_holders, name=self.name)

    def freeze(self) -> Tensor:

        constants = []
        for holder in self.holders:
            constants.append(holder.freeze().constants)

        max_length = max(len(sub_constants) for sub_constants in constants)
        for sub_constants in constants:
            while len(sub_constants) < max_length:
                sub_constants.append(0)

        Progress.update()
        return Tensor(array(constants))

    def scale(self, value: Union[float, Decimal]) -> IterativeConstant:
        new_holders = []
        for holder in self.holders:
            new_holders.append(holder.scale(value))

        Progress.update()
        return IterativeConstant(initial_holders=new_holders, name=self.name)

    def poly_scale(self, value: Union[float, Decimal]) -> IterativeConstant:
        value = Decimal(value)

        new_holders = []
        for i, holder in enumerate(self.holders):
            p_value = value ** Decimal(i)
            new_holders.append(holder.scale(p_value))

        Progress.update()
        return IterativeConstant(initial_holders=new_holders, name=self.name)

    def update(self, i: int, holder: ScalerHolder) -> IterativeConstant:
        if i >= len(self.holders):
            raise ValueError(f"Update at index {i} out of range {len(self.holders)}")

        iterator = self.copy()
        iterator.holders[i] = holder
        self.verify_names(iterator)

        Progress.update()
        return iterator

    def append(self, holder: ScalerHolder) -> IterativeConstant:
        iterator = self.copy()
        iterator.holders.append(holder)
        self.verify_names(iterator)

        Progress.update()
        return iterator

    def conv(self, iterator: IterativeConstant, i: int, n: int) -> ScalerHolder:
        self_iterator = self.copy()

        if len(self_iterator.holders) != len(iterator.holders):
            raise ValueError("Sizes of iterators do not match.")
        if len(iterator.holders) == 0:
            raise ValueError("Cannot take convolution of empty iterators")
        if n > len(self_iterator.holders):
            raise ValueError("Upper index, n, cannot be larger than size of iterators")
        if i > n:
            raise ValueError("Lower index, i, cannot be larger than upper index.")

        N = len(self_iterator.holders) - 1

        holder = ScalerHolder(initial_constants=[0], name=iterator.holders[0].name)
        for i in range(i, n + 1):
            a_i = self_iterator.get(i)
            b_n_minus_i = iterator.get(N - i)
            c_n_i = a_i.multiply(b_n_minus_i)
            holder = holder.add(c_n_i)

        Progress.update()
        return holder
