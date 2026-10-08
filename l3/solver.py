"""
Универсальный решатель многошаговых методов.

Принимает:
    start_values : список (t_i, y_i) для i = 0, ..., k−1  — стартовые точки
    rhs          : правая часть f(t, y)  — для системы: список из двух функций
    step_func    : функция шага метода (см. adams_bashforth.METHODS)
    h            : шаг
    t_end        : конец отрезка
"""


def solve_multistep(start_values, rhs, step_func, h, t_end):
    """
    start_values : list[(float, tuple)] — [(t_0, (x_0, y_0)), ...]
    rhs          : callable(t, y) → tuple(x', y')  — векторная правая часть
    step_func    : функция шага (f, t, y, h) → новое y
    """
    ts = [sv[0] for sv in start_values]
    ys = [sv[1] for sv in start_values]
    fs = [rhs(sv[0], sv[1]) for sv in start_values]

    while ts[-1] < t_end - 1e-12:
        t_next = ts[-1] + h
        y_next = step_func(fs, ys, h)
        f_next = rhs(t_next, y_next)

        ts.append(t_next)
        ys.append(y_next)
        fs.append(f_next)

    return ts, ys