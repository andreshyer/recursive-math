![Python Tests](https://github.com/andreshyer/recursive-math/workflows/Python%20Tests/badge.svg)

# recursive-math

This repo is designed to abstract many of the ideas of solving recursive coefficients,
with a goal of allowing for the pseudo-functional programming of coefficients.
After solving for the coefficients in terms of an arbitrary constant, if one exists,
computationally efficient calculating values form the curve.

# Installation

`pip install git+https://github.com/andreshyer/recursive-math.git`

# Overview

For many ODEs with initial value boundary conditions, 
they can be solved in series form recursively.
Taking a simple case.

$$y'' = By$$

With the boundary conditions $y(0) = 1$ and $y'(0) = 0$, 
the following series can be assumed.

$$y = \sum_{n=0}^\infty a_n x^n$$

Where the first coefficients are defined by the boundary conditions,
$a_0 = 1$ and $a_1 = 0$.
Plugging in the series back into the equation 
leads to the following recursion solution for $a_n$ terms.

$$a_{n+2} = \frac{B}{(n+1)(n+2)} a_n$$

The equation above can be solved very easily in a closed form solution.
There are many equations that cannot be easily solved in closed form,
but can be easily solved in series form.

$$y*y''+ 2y'= B \sin{x}, \\ y(0)=1, \\ y'(0)=1$$

$$y = \sum_{n=0}^\infty a_n x^n, \\ \\ a_0=a_1=1$$

$$\left(\sum_{n=0}^\infty a_n x^n\right) \left( \sum_{n=0}^\infty b_n x^n \right) + \sum_{n=0}^\infty c_n x^n = \sum_{n=0}^\infty B f_n x^n$$

$$b_n = (n+1)(n+2) a_{n+2}$$

$$c_n = 2 (n+1) a_{n+1}$$

$$\sum_{n=0}^\infty d_n x^n + \sum_{n=0}^\infty c_n x^n = \sum_{n=0}^\infty B f_n x^n$$

$$d_n = \sum_{i=0}^n a_i b_{n-i}$$

$$d_n = B f_n - c_n$$

$$\sum_{i=0}^n a_i b_{n-i} = B f_n - c_n$$
 
$$a_0 b_n + \sum_{i=1}^n a_i b_{n-i} = B f_n - c_n$$

$$a_{n+2} = \frac{1}{(n+1)(n+2)} \left( B f_n - c_n - g_n \right) = F(B, n, a_0, a_1, ..., a_n)$$

For many equations, it is easier and faster to use numerical approximation than to use a series solution.
This repo attempts to bridge the gap where each coefficient can be solved in terms of B, a_n = a_n(B).
When B is specified, the coefficients can quickly be solved and used. 
With the general philosophy that it is acceptable for a large amount of resources and time to generate coefficient equations,
if it only needs to be done once.

In this repo, there are only a few main concepts.
1) Raw coefficients (ScalerHolders) should be able to be written in terms of a constant.
2) Raw series (IterativeConstants) contain many coefficients which are in terms of a constant.
3) Mathematical operations can be done on either series or coefficients.
5) Calculating the coefficients in the series requires high precision.
6) Using the coefficients does not require precision and should be fast.

ScalerHolder example:

$$a_2 = 1 + B/4$$

```python
from decimal import Decimal
from recursive_math import ScalerHolder
D = Decimal

a_2 = ScalerHolder(initial_constants=[1, D(1)/D(4)], name="B")
print(a_2)
>>>1.000e+0 B⁰ + 2.500e-1 B¹
```

IterativeConstant example:

$$a_0 = 1, \\ a_1 = 1$$

```python
from decimal import Decimal
from recursive_math import ScalerHolder, IterativeConstant
D = Decimal

a_0 = ScalerHolder(initial_constants=[1], name="B")
a_1 = ScalerHolder(initial_constants=[1], name="B")

a_n = IterativeConstant(initial_holders=[a_0, a_1], name="a")
print(a_n)
>>>[a₀: 1.000e+0 B⁰, a₁: 1.000e+0 B⁰]
```

Math Operations examples:

The easiest way to show an example of the mathamatical operations that are possible
is by solving a real-world problem. 
Looking at the example from earlier

```python
from decimal import Decimal
from recursive_math import ScalerHolder, IterativeConstant, Sin, set_decimal_precision
D = Decimal

sin_x = Sin(name="f", holder_name="B")

a_0 = ScalerHolder(initial_constants=[1], name="B")
a_1 = ScalerHolder(initial_constants=[1], name="B")
a_n = IterativeConstant(initial_holders=[a_0, a_1], name="a")

c_n = IterativeConstant(initial_holders=[], name="c")
h_n = IterativeConstant(initial_holders=[], name="h")
g_n = IterativeConstant(initial_holders=[], name="g")
b_n = IterativeConstant(initial_holders=[], name="b")

N = 10
for n in range(N):
    sin_x = sin_x.next_term()

    c_i = a_n.get(n + 1)
    c_i = c_i.scale(2 * (n + 1))
    c_n = c_n.append(c_i)

    h_i = sin_x.get(n)
    h_i = h_i.increase_scaler()
    h_n = h_n.append(h_i)  # Bf_n

    if n == 0:
        g_i = ScalerHolder(initial_constants=[0], name="B")
    else:
        a_n_sub = a_n[:(n+1)]

        empty_holder = ScalerHolder(initial_constants=[0], name="B")
        b_n_ext = b_n.append(empty_holder)

        g_i = a_n_sub.conv(b_n_ext, i=1, n=n)  # IterativeConstants have to be the same size for convolution

    g_n = g_n.append(g_i)  # \sum_{i=1}^n a_i b_{n-i}

    a_i_p_2 = h_i.add(c_i.scale(-1))
    a_i_p_2 = a_i_p_2.add(g_i.scale(-1))
    a_i_p_2 = a_i_p_2.scale(1 / D(n + 1))
    a_i_p_2 = a_i_p_2.scale(1 / D(n + 1))
    a_n = a_n.append(a_i_p_2)

    b_i = a_n.get(n + 2)
    b_i = b_i.scale(D(n + 1))
    b_i = b_i.scale(D(n + 2))
    b_n = b_n.append(b_i)

print(a_n)
>>>[a₀: 1.000e+0 B⁰, a₁: 1.000e+0 B⁰, a₂: -1.000e+0 B⁰ + 0.000e+2 B¹, a₃: 6.667e-1 B⁰ + 1.667e-1 B¹,
a₄: -8.333e-1 B⁰ + -1.667e-1 B¹, a₅: 3.333e-1 B⁰ + 5.833e-2 B¹, a₆: -8.111e-1 B⁰ + -1.806e-1 B¹ + -5.556e-3 B², ...]
```

The coefficients are linearly depends on B all the way up to $a_6$, which is surprising.

Precision:

The precision is set very high by default

```python
# Default precision
from decimal import getcontext
getcontext().prec = 1000
```

This precision is not used for the final calculations,
but only to generate the coefficient equations.
This precision can easily be lowered if not needed,
either using the method above or using a built-in function.

```python
from recursive_math import set_decimal_precision
set_decimal_precision(100)
```

Using coefficients:

While calculating the coefficients is often complex and take a long time,
using the constants is highly optimized.

```python
y = a_n.freeze()
y = y.reduce(scaler_value=1)  # Specify what B is

x = np.array([0.1, 0.5, 1])
y = y.evaluate(x=x)
print(y)
>>>[1.08188045 1.09863281 0.29513889]
```
