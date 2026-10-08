"""
Лабораторная № 3. Метод Адамса-Бэшфорта.

Задание 1: система ОДУ.  Стартовые значения — из build_taylor_system.
Задание 2: ОДУ 2-го порядка.  Стартовые значения — из build_taylor_ode.

ОДУ 2-го порядка сводится к системе (y, y') и решается тем же методом.
"""

import numpy as np
import sympy as sp

from data.option import (
    initial_condition, integration_interval, analytical_decision,
    data_ode, analytical_ode, ode_rhs, f_1, f_2,
)
from utils.table_generator import print_table, fmt
from utils.calculation_error import max_error_percent, abs_error

from l2.taylor_system import build_taylor_system
from l2.taylor_ode import build_taylor_ode
from l3.adams_bashforth import METHODS
from l3.solver import solve_multistep


# ============================================================
# Правые части (векторные)
# ============================================================

def system_rhs(t, state):
    """Система: x' = f_1(t, y), y' = f_2(t, x)."""
    x, y = state
    return (f_1(t, y), f_2(t, x))


def ode_system_rhs(t, state):
    """ОДУ 2-го порядка: y'' = ode_rhs(t, y, y').

    Сводим к системе:  y' = z,  z' = ode_rhs(t, y, z).
    """
    y, z = state
    return (z, ode_rhs(t, y, z))


# ============================================================
# Стартовые значения
# ============================================================

def start_values_system(order, h):
    """
    k = order стартовых точек для системы.
    Ряд строим до порядка order+1, чтобы старт был точнее метода.
    """
    x_n_sym, y_n_sym, _, t_sym = build_taylor_system(n=order + 1)

    x_fn = sp.lambdify(t_sym, x_n_sym, 'numpy')
    y_fn = sp.lambdify(t_sym, y_n_sym, 'numpy')

    t0, _, _ = initial_condition()
    result = []
    for i in range(order):
        ti = t0 + i * h
        result.append((ti, (float(x_fn(ti)), float(y_fn(ti)))))
    return result


def start_values_ode(order, h):
    """
    k = order стартовых точек для ОДУ 2-го порядка.
    Вектор состояния: (y, y').
    """
    y_n_sym, y1_n_sym, _, t_sym = build_taylor_ode(n=order + 1)

    y_fn = sp.lambdify(t_sym, y_n_sym, 'numpy')
    y1_fn = sp.lambdify(t_sym, y1_n_sym, 'numpy')

    t0, _, _ = data_ode()
    result = []
    for i in range(order):
        ti = t0 + i * h
        result.append((ti, (float(y_fn(ti)), float(y1_fn(ti)))))
    return result


# ============================================================
# Задание 1: система
# ============================================================

def solve_system(order, h, t_end=None):
    t0, _, _ = initial_condition()
    _, t_end_default = integration_interval()
    if t_end is None:
        t_end = t_end_default

    start = start_values_system(order, h)
    step_func = METHODS[order]
    ts, ys = solve_multistep(start, system_rhs, step_func, h, t_end)

    xs = np.array([y[0] for y in ys])
    yv = np.array([y[1] for y in ys])
    return np.array(ts), xs, yv


# ============================================================
# Задание 2: ОДУ 2-го порядка
# ============================================================

def solve_ode(order, h, t_end=None):
    t0, _, _ = data_ode()
    _, t_end_default = integration_interval()
    if t_end is None:
        t_end = t_end_default

    start = start_values_ode(order, h)
    step_func = METHODS[order]
    ts, ys = solve_multistep(start, ode_system_rhs, step_func, h, t_end)

    yv = np.array([s[0] for s in ys])
    y1v = np.array([s[1] for s in ys])
    return np.array(ts), yv, y1v


# ============================================================
# Печать и запуск
# ============================================================

def solve_several_h(order=4):
    print("=" * 60)
    print(f"Метод Адамса-Бэшфорта, порядок {order}")
    print("=" * 60)

    for i in range(1, 4):
        h = 10 ** (-i)
        print(f"\n########## h = {h} ##########")

        # --- Система ---
        print("\n--- Система ОДУ ---")
        ts, xs, ys = solve_system(order, h)
        x_exact, y_exact = analytical_decision(ts)
        i_last = -1
        print(f"  t = {ts[i_last]:.2f}")
        print(f"  x : точное = {x_exact[i_last]:.6f}   прибл. = {xs[i_last]:.6f}   Δx = {abs(x_exact[i_last] - xs[i_last]):.4e}")
        print(f"  y : точное = {y_exact[i_last]:.6f}   прибл. = {ys[i_last]:.6f}   Δy = {abs(y_exact[i_last] - ys[i_last]):.4e}")

        # --- ОДУ 2-го порядка ---
        print("\n--- ОДУ 2-го порядка ---")
        ts_ode, yv, y1v = solve_ode(order, h)
        y_exact_ode, y1_exact_ode = analytical_ode(ts_ode)
        i_last = -1
        print(f"  t = {ts_ode[i_last]:.2f}")
        print(f"  y : точное = {y_exact_ode[i_last]:.6f}   прибл. = {yv[i_last]:.6f}   Δy  = {abs(y_exact_ode[i_last] - yv[i_last]):.4e}")
        print(f"  y': точное = {y1_exact_ode[i_last]:.6f}   прибл. = {y1v[i_last]:.6f}   Δy' = {abs(y1_exact_ode[i_last] - y1v[i_last]):.4e}")


if __name__ == "__main__":
    solve_several_h(order=5)