"""
Метод Адамса-Бэшфорта (явный многошаговый).

Формулы из методички (3.1)–(3.4):
    порядок 2: y_{n+1} = y_n + h/2 · [3 f_n − f_{n−1}]
    порядок 3: y_{n+1} = y_n + h/12 · [23 f_n − 16 f_{n−1} + 5 f_{n−2}]
    порядок 4: y_{n+1} = y_n + h/24 · [55 f_n − 59 f_{n−1} + 37 f_{n−2} − 9 f_{n−3}]
    порядок 5: y_{n+1} = y_n + h/720 · [1901 f_n − 2774 f_{n−1} + 2616 f_{n−2} − 1274 f_{n−3} + 251 f_{n−4}]
"""


def _apply_ab(f, y, h, coeffs, denom):
    """
    Универсальный шаг Адамса-Бэшфорта.
    f, y — списки кортежей.
    coeffs — коэффициенты [c1, c2, ...] для f[-1], f[-2], ...
    denom — знаменатель (1, 2, 12, 24, 720)
    """
    y_n = y[-1]
    return tuple(
        y_n[i] + h / denom * sum(c * f[-1 - j][i] for j, c in enumerate(coeffs))
        for i in range(len(y_n))
    )


def ab2(f, y, h):
    return _apply_ab(f, y, h, [3, -1], 2)


def ab3(f, y, h):
    return _apply_ab(f, y, h, [23, -16, 5], 12)


def ab4(f, y, h):
    return _apply_ab(f, y, h, [55, -59, 37, -9], 24)


def ab5(f, y, h):
    return _apply_ab(f, y, h, [1901, -2774, 2616, -1274, 251], 720)


# Реестр: порядок → функция шага
METHODS = {
    2: ab2,
    3: ab3,
    4: ab4,
    5: ab5,
}