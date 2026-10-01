import math
from numpy import exp, sin, cos


def data():
    a, b = 0, 0
    x0, y0 = 1, 0
    return a, b, x0, y0
# def data():
#     a, b = 0, 0
#     x0, y0 = 2, 2
#     return a, b, x0, y0


def f_1(t_i, y_i):

    return math.exp(3*t_i) - y_i


def f_2(t_i, x_i):
    return 2*math.exp(3*t_i) - x_i


def f_1_symbol(t, x, y):
    import sympy as sp
    return sp.exp(3*t) - y


def f_2_symbol(t, x, y):
    import sympy as sp
    return 2*sp.exp(3*t) - x


def analytical_decision(t):
    x = 3/4 * exp(t) + 1/8 * exp(-t) + 1/8 * exp(3*t)
    y = -3/4 * exp(t) + 1/8 * exp(-t) + 5/8 * exp(3*t)

    return x, y


def analytical_decision_for_de(x):
    return sin(2*x), 2*cos(2*x)


def symbol_analytical_decision(t):
    from sympy import exp
    x = 3 / 4 * exp(t) + 1 / 8 * exp(-t) + 1 / 8 * exp(3 * t)
    y = -3 / 4 * exp(t) + 1 / 8 * exp(-t) + 5 / 8 * exp(3 * t)
    return x, y


def symbol_analytical_decision_for_example1(t):
    from sympy import exp
    x = exp(2*t) + 1
    y = 2*exp(2*t)
    return x, y


def analytical_decision_for_example1(t):
    x = exp(2*t) + 1
    y = 2*exp(2*t)
    return x, y


def symbol_analytical_decision_for_example2(t):
    from sympy import exp
    y = 2*exp(t**2/2) - 1
    y1 = 2*t*exp(t**2/2)
    return y, y1


def analytical_decision_for_example2(t):
    y = 2*exp(t**2/2) - 1
    y1 = 2*t*exp(t**2/2)
    return y, y1

