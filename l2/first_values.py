import sympy as sp
from data.option import symbol_analytical_decision, symbol_analytical_decision_for_example1, \
    analytical_decision_for_example1, analytical_decision_for_example2, data, analytical_decision, \
    analytical_decision_for_de, f_1_symbol, f_2_symbol
import numpy as np

from utils.build_graph import build_option_graph
from utils.calculation_error import max_error_percent, rel_error, abs_error
from utils.table_generator import print_table, generate_table_for_error, fmt


def for_system(n, h):
    a, b, x0, y0 = data()
    t = sp.Symbol('t')
    x, y = sp.Function('x')(t), sp.Function('y')(t)
    # x, y = symbol_analytical_decision(t)
    f1, f2 = f_1_symbol(t, x, y), f_2_symbol(t, x, y)
    x_n, y_n = sp.Integer(x0), sp.Integer(y0)
    products_list = [(x0, y0)]
    print(x)
    print(y)
    for i in range(1, n+1):
        products_list.append((f1.subs({t: a, x: products_list[i-1][0], y: products_list[i-1][1]}), f2.subs({t: b, x: products_list[i-1][0], y: products_list[i-1][1]})))
        x_n += products_list[i][0] / sp.factorial(i) * t ** i
        y_n += products_list[i][1] / sp.factorial(i) * t ** i

        f1 = sp.diff(f1, t)
        f2 = sp.diff(f2, t)

    print(x_n, y_n, sep="\n")

    for i in range(5):
        print(float(x_n.subs(t, i*h)), float(y_n.subs(t, i*h)))

    # Превращаем в numpy-функцию
    x_n = sp.lambdify(t, x_n, 'numpy')
    y_n = sp.lambdify(t, y_n, 'numpy')

    # Массив точек
    t = np.arange(a, a + 5 * h, h)

    return t, x_n(t), y_n(t)


def for_diff_eq(n, h):
    import sympy as sp

    t0, y0, y1 = 0, 0, 2
    t = sp.Symbol('t')
    y = sp.Function('y')(t)  # x — функция от t

    # Правая часть: f(t, x, x')
    # def f(t, y, yp):
    #     return t*sp.diff(y, t) + y + 1 # пример: x'' = -x

    def f(t, y, yp):
        return -4*y # пример: x'' = -x

    ys = sp.symbols(f'y0:{n}')

    def to_symbol(expr):
        # от старших порядков к младшим
        for k in range(n - 1, 0, -1):
            expr = expr.subs(sp.Derivative(y, (t, k)), ys[k])
        return expr.subs(y, ys[0])

    # Выражения для производных как функций от t
    Y = {
        0: y,
        1: sp.diff(y, t),  # y'
        2: f(t, y, sp.diff(y, t)),  # y'' = f
    }

    # Дальше: Y[k] = d/dt Y[k-1] — прямое дифференцирование по t
    for k in range(3, n+1):
        Y[k] = sp.diff(Y[k - 1], t)

    print(Y)

    Y = {k: to_symbol(Y[k]) for k in range(n+1)}
    print(Y)
    val_Y = {0: float(Y[0].subs(ys[0], y0)), 1: float(Y[1].subs(ys[1], y1))}
    for k in range(2, n+1):
        val_Y[k] = float(Y[k].subs({t: t0, ys[k-1]: val_Y[k-1], ys[k-2]: val_Y[k-2]}))

    for k in range(n+1):
        print(f"Y{k} = y^({k}) = {Y[k]} = {val_Y[k]}")

    y_n = sp.Integer(0)
    for k in range(n + 1):
        y_n += val_Y[k] / sp.factorial(k) * t ** k

    y1_n = sp.diff(y_n, t)
    print(y_n)
    print(y1_n)

    # Превращаем в numpy-функцию
    y_n = sp.lambdify(t, y_n, 'numpy')
    y1_n = sp.lambdify(t, y1_n, 'numpy')

    # Массив точек
    t = np.arange(t0, t0 + 5*h, h)

    return t, y_n(t), y1_n(t)


def solve_several_h(n):
    for i in range(1, 4):
        h = 10**(-i)

        t_besh, x_n_besh, y_n_besh = for_system(n, h)
        # t_mull, y_n_mull, y1_n_mull = for_diff_eq(n, h)
        x_besh, y_besh = analytical_decision(t_besh)
        # y_mull, y1_mull = analytical_decision_for_de(t_mull)
        print_table(x_besh, y_besh, x_n_besh, y_n_besh, t_besh)
        # print_table(y_mull, y1_mull, y_n_mull, y1_n_mull, t_mull)

        print("\delta x:")
        print(fmt(max_error_percent(x_besh, x_n_besh, abs_error)))
        print("\delta y:")
        print(fmt(max_error_percent(y_besh, y_n_besh, abs_error)))
        # print(generate_table_for_error(x_besh, y_besh, {x_n_besh, y_n_besh}, h))
        # print(generate_table_for_error(y_mull, y1_mull, y_n_mull, y1_n_mull, h))
        # build_option_graph(x_besh, y_besh, x_n_besh, y_n_besh, t_besh, h, "Бешфорта")
        # build_option_graph(y_mull, y1_mull, y_n_mull, y1_n_mull, t_mull, h, "Мулла")


if __name__ == "__main__":
    n, h = 5, 0.1
    solve_several_h(n)


