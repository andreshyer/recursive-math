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
 
