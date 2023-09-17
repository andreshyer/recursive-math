from __future__ import annotations
from typing import Union

import numba
from numpy import ndarray, empty, float64


@numba.jit(nopython=True)
def evaluate_polynomial(x: float, constants: ndarray) -> float:
    constants = constants[::-1]

    value = constants[0]
    for i in range(1, len(constants)):
        value = value * x + constants[i]
    return value


@numba.jit(nopython=True)
def evaluate_polynomials(scaler_value: float, matrix: ndarray) -> ndarray:
    results = empty(matrix.shape[0], dtype=float64)
    for i in range(len(matrix)):
        results[i] = evaluate_polynomial(scaler_value, matrix[i])
    return results


@numba.jit(nopython=True)
def n_evaluate_polynomial(x: ndarray, constants: ndarray) -> ndarray:
    results = empty(x.shape[0], dtype=float64)
    for i in range(len(x)):
        results[i] = evaluate_polynomial(float(x[i]), constants)
    return results


class Series:

    def __init__(self, constants: ndarray):
        self.constants: ndarray = constants

    def __str__(self) -> str:
        return str(self.constants)

    def __eq__(self, series: Series) -> bool:
        if isinstance(series, Series):
            return self.constants.tolist() == series.constants.tolist()
        return NotImplemented

    def evaluate(self, x: Union[float, ndarray]) -> Union[float, ndarray]:
        if isinstance(x, ndarray):
            return n_evaluate_polynomial(x, self.constants)
        return evaluate_polynomial(x, self.constants)


class Tensor:

    def __init__(self, constants: ndarray):
        self.constants: ndarray = constants

    def __str__(self) -> str:
        return str(self.constants)

    def __eq__(self, tensor: Tensor) -> bool:
        if isinstance(tensor, Tensor):
            return self.constants.tolist() == tensor.constants.tolist()
        return NotImplemented

    def reduce(self, scaler_value: float) -> Series:
        return Series(evaluate_polynomials(scaler_value, self.constants))

    def flatten(self) -> Series:
        for c in self.constants:
            if len(c) != 1:
                raise ValueError(f"Cannot flatten {self}")
        return Series(evaluate_polynomials(1, self.constants))
