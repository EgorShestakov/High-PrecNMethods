"""Лабораторная № 2. Формирование таблицы начальных значений
для многошаговых методов (ряды Маклорена)."""

import numpy as np
import sympy as sp

from data.option import initial_condition, analytical_decision, data_ode, analytical_ode
from utils.table_generator import print_table, fmt
from utils.calculation_error import max_error_percent, abs_error

from l2.taylor_system import build_taylor_system
from l2.taylor_ode import build_taylor_ode


def for_system(n, h, n_points=5):
    """Задание 1: таблица пяти начальных значений для системы."""
    t0, x0, y0 = initial_condition()
    x_n_sym, y_n_sym, values, t_sym = build_taylor_system(n)

    print("\n=== Система: ряды Маклорена ===")
    print("x(t) =", x_n_sym)
    print("y(t) =", y_n_sym)
    print("Значения производных в t0:")
    for k, (xv, yv) in enumerate(values):
        print(f"  x^({k})(t0) = {xv},   y^({k})(t0) = {yv}")

    x_fn = sp.lambdify(t_sym, x_n_sym, 'numpy')
    y_fn = sp.lambdify(t_sym, y_n_sym, 'numpy')

    t = np.arange(t0, t0 + n_points * h, h)
    x_approx = x_fn(t)
    y_approx = y_fn(t)

    return t, x_approx, y_approx


def for_diff_eq(n, h, n_points=5):
    t0, y0, y1 = data_ode()
    y_n_sym, y1_n_sym, val_Y, t_sym = build_taylor_ode(n)

    print("\n=== ОДУ 2-го порядка: ряды Маклорена ===")
    print("y(t)  =", y_n_sym)
    print("y'(t) =", y1_n_sym)
    print("Значения производных в t0:")
    for k, v in val_Y.items():
        print(f"  y^({k})(t0) = {v}")

    y_fn = sp.lambdify(t_sym, y_n_sym, 'numpy')
    y1_fn = sp.lambdify(t_sym, y1_n_sym, 'numpy')

    t = np.arange(t0, t0 + n_points * h, h)
    y_approx = y_fn(t)
    y1_approx = y1_fn(t)

    y_exact, y1_exact = analytical_ode(t)

    return t, y_exact, y1_exact, y_approx, y1_approx


def solve_several_h(n=5):
    for i in range(1, 4):
        h = 10 ** (-i)
        print(f"\n\n########## h = {h} ##########")

        # --- Система ---
        t, x_approx, y_approx = for_system(n, h)
        x_exact, y_exact = analytical_decision(t)
        print("\n--- Таблица (система) ---")
        print_table(x_exact, y_exact, x_approx, y_approx, t)
        print("δx =", fmt(max_error_percent(x_exact, x_approx, abs_error)))
        print("δy =", fmt(max_error_percent(y_exact, y_approx, abs_error)))

        # --- ОДУ 2-го порядка ---
        t_ode, y_exact_ode, y1_exact_ode, y_approx_ode, y1_approx_ode = for_diff_eq(n, h)
        print("\n--- Таблица (ОДУ 2-го порядка) ---")
        print_table(y_exact_ode, y1_exact_ode, y_approx_ode, y1_approx_ode, t_ode)
        print("δy  =", fmt(max_error_percent(y_exact_ode, y_approx_ode, abs_error)))
        print("δy' =", fmt(max_error_percent(y1_exact_ode, y1_approx_ode, abs_error)))


if __name__ == "__main__":
    solve_several_h(n=5)
