![Python Tests](https://github.com/andreshyer/recursive-math/workflows/Python%20Tests/badge.svg)

# recursive-math

This repo is designed to abstract many of the ideas of solving recursive coefficients,
with a goal of allowing for the pseudo-functional programming of coefficients.
After solving for the coeifficents in terms of an abitary constant, if one exists,
computationally efficent calculating values form the curve.

# Overview

For many ODEs with inital value boundary conditions, 
they can be solved in series form recursively.
Taking a simple case.

$$y'' = By$$

With the boundary conditions $y(0) = 1$ and $y'(0) = 0$, 
the following series can be assumed.

$$y = \sum_{n=0}^\infty a_n x^n$$

Where the first coeifficents are defined by the bondary conditions,
$a_0 = 1$ and $a_1 = 0$.
Plugging in the series back into the equation 
leads to the following recusion solution for $a_n$ terms.

$$a_{n+2} = \frac{B}{(n+1)(n+2)} a_n$$

The equation above can be solved very easily in a closed form solution.
There are many equations that cannot be easily solved in closed form,
but can be easily solved in series form.

$$y*y''+ 2y'= B \sin{x}, \\ y(0)=1, \\ y(0)=1$$

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

For many equations, it is easier and faster to use numerical appromiaxtion than to use a series solution.
This repo attempts to bridge the gap where each coeifficent can be solved in terms of B, a_n = a_n(B).
When B is specified, the coeifficents can quickly be solved and used. 
With the general philosophy that it is acceptable for a large amount of resources and time to generate coeifficent equations,
if it only needs to be done once.

In this repo, there are four main concepts.
1) Raw coeifficents (ScalerHolders) should be able to be written in terms of a constant.
2) Raw series (IterativeConstants) contain many coeifficents which are in terms of a constant.
3) Mathamatical operations can be done on either series or coeifficents.
5) Calculating the coeifficents in the series requries high precision.
6) Using the coeifficents does not require precision and should be fast.

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
