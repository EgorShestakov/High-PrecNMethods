"""Метод Тейлора (ряды Маклорена) для системы ОДУ.

    x' = f_1(t, x, y)
    y' = f_2(t, x, y)

Строит частичные суммы рядов Маклорена для x(t) и y(t),
используя последовательное дифференцирование правых частей
и подстановку начальных условий. Аналитическое решение
НЕ используется.
"""

import sympy as sp
from data.option import f_1_symbol, f_2_symbol, initial_condition


def build_taylor_system(n):
    """
    Строит ряды Тейлора для системы до порядка n включительно.

    Возвращает:
        x_n_sym, y_n_sym : sympy-выражения (ряды по t)
        values          : list[(x^(k)(t0), y^(k)(t0))] для k = 0..n
        t               : sympy-символ t
    """
    t0, x0, y0 = initial_condition()
    t = sp.Symbol('t')
    x = sp.Function('x')(t)
    y = sp.Function('y')(t)

    f1 = f_1_symbol(t, x, y)
    f2 = f_2_symbol(t, x, y)

    values = [(sp.Integer(x0), sp.Integer(y0))]

    for i in range(1, n + 1):
        subs_dict = {t: t0}
        for k in range(i):
            if k == 0:
                subs_dict[x] = values[0][0]
                subs_dict[y] = values[0][1]
            else:
                subs_dict[sp.Derivative(x, (t, k))] = values[k][0]
                subs_dict[sp.Derivative(y, (t, k))] = values[k][1]

        xi = f1.subs(subs_dict)
        yi = f2.subs(subs_dict)

        if xi.free_symbols or yi.free_symbols:
            raise RuntimeError(
                f"i={i}: остались символы. "
                f"xi free={xi.free_symbols}, yi free={yi.free_symbols}"
            )

        values.append((sp.Integer(xi), sp.Integer(yi)))

        f1 = sp.diff(f1, t)
        f2 = sp.diff(f2, t)

    x_n = sp.Integer(x0)
    y_n = sp.Integer(y0)
    for k in range(1, n + 1):
        x_n += values[k][0] / sp.factorial(k) * t ** k
        y_n += values[k][1] / sp.factorial(k) * t ** k

    return x_n, y_n, values, t
