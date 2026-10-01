"""Метод Тейлора (ряды Маклорена) для ОДУ 2-го порядка.

    y'' = ode_rhs(t, y, y')
    y(t0) = y0,  y'(t0) = y1

Строит частичную сумму ряда Маклорена для y(t),
используя последовательное дифференцирование правой части.
Аналитическое решение НЕ используется.
"""

import sympy as sp
from data.option import data_ode, ode_rhs


def build_taylor_ode(n):
    """
    Строит ряд Тейлора для y(t) до порядка n включительно.

    Возвращает:
        y_n_sym : sympy-выражение (ряд по t)
        val_Y   : dict {k: y^(k)(t0)} для k = 0..n
        t       : sympy-символ t
    """
    t0, y0, y1 = data_ode()
    t = sp.Symbol('t')
    y = sp.Function('y')(t)

    ys = sp.symbols(f'y0:{n + 2}')

    def to_symbol(expr):
        for k in range(n + 1, 0, -1):
            expr = expr.subs(sp.Derivative(y, (t, k)), ys[k])
        return expr.subs(y, ys[0])

    # Строим производные функционально
    Y_func = {
        0: y,
        1: sp.diff(y, t),
        2: ode_rhs(t, y, sp.diff(y, t)),
    }
    for k in range(3, n + 1):
        Y_func[k] = sp.diff(Y_func[k - 1], t)

    # Переводим в символы
    Y_sym = {k: sp.expand(to_symbol(Y_func[k])) for k in range(n + 1)}

    # Подстановка значений
    val_Y = {0: sp.Integer(y0), 1: sp.Integer(y1)}
    for k in range(2, n + 1):
        subs_dict = {t: t0}
        for j in range(k):
            subs_dict[ys[j]] = val_Y[j]
        val_Y[k] = Y_sym[k].subs(subs_dict)

        if val_Y[k].free_symbols:
            raise RuntimeError(
                f"k={k}: остались символы {val_Y[k].free_symbols}"
            )

    # Строим ряд
    y_n = sp.Integer(0)
    for k in range(n + 1):
        y_n += val_Y[k] / sp.factorial(k) * t ** k

    return y_n, val_Y, t
