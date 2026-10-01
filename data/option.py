"""
Данные задачи и правые части.

Здесь живёт ВСЁ, что относится к конкретной задаче:
- начальные условия (data, data_ode)
- правые части системы (f_1, f_2) — численно
- правые части системы (f_1_symbol, f_2_symbol) — символьно
- аналитическое решение (analytical_decision) — численно
- аналитическое решение (symbol_analytical_decision) — символьно
- правая часть ОДУ 2-го порядка (ode_rhs) и его решение (analytical_ode)

Метод-специфичный код (шаг Эйлера, шаг Хойна, формула Тейлора)
в этот файл НЕ добавлять — он должен лежать в l1/ или l2/.
"""

import math
import sympy as sp
from numpy import exp, sin, cos


# ============================================================
# Система ОДУ (пример 1.1 / 2.1 методички)
#   x' = f_1(t, y)
#   y' = f_2(t, x)
# ============================================================

def initial_condition():
    """Задача Коши: t0, x(t0), y(t0)."""
    t0 = 0.0
    x0, y0 = 1.0, 0.0
    return t0, x0, y0


def integration_interval():
    """Отрезок интегрирования [t_start, t_end]."""
    return 0.0, 2.0


# ---------- Численные правые части ----------
def f_1(t, y):
    return math.exp(3 * t) - y


def f_2(t, x):
    return 2 * math.exp(3 * t) - x


# ---------- Символьные правые части ----------
def f_1_symbol(t, x, y):
    return sp.exp(3 * t) - y


def f_2_symbol(t, x, y):
    return 2 * sp.exp(3 * t) - x


# ---------- Аналитическое решение (численно) ----------
def analytical_decision(t):
    x = 3 / 4 * exp(t) + 1 / 8 * exp(-t) + 1 / 8 * exp(3 * t)
    y = -3 / 4 * exp(t) + 1 / 8 * exp(-t) + 5 / 8 * exp(3 * t)
    return x, y


# ---------- Аналитическое решение (символьно) ----------
def symbol_analytical_decision(t):
    x = 3 / 4 * sp.exp(t) + 1 / 8 * sp.exp(-t) + 1 / 8 * sp.exp(3 * t)
    y = -3 / 4 * sp.exp(t) + 1 / 8 * sp.exp(-t) + 5 / 8 * sp.exp(3 * t)
    return x, y


# ---------- Устаревшие алиасы (для совместимости) ----------
def analytical_decision_for_example1(t):
    return exp(2 * t) + 1, 2 * exp(2 * t)


def symbol_analytical_decision_for_example1(t):
    return sp.exp(2 * t) + 1, 2 * sp.exp(2 * t)


def analytical_decision_for_example2(t):
    y = 2 * exp(t ** 2 / 2) - 1
    y1 = 2 * t * exp(t ** 2 / 2)
    return y, y1


def symbol_analytical_decision_for_example2(t):
    y = 2 * sp.exp(t ** 2 / 2) - 1
    y1 = 2 * t * sp.exp(t ** 2 / 2)
    return y, y1


# ============================================================
# ОДУ 2-го порядка (пример 2.2 методички)
#   y'' = t*y' + y + 1
# ============================================================

def data_ode():
    """t0, y(t0), y'(t0)."""
    t0 = 0.0
    y0 = 1.0
    y1 = 0.0
    return t0, y0, y1


def ode_rhs(t, y, yp):
    """y'' = t*y' + y + 1."""
    return t * yp + y + 1


def analytical_ode(t):
    """y(t), y'(t) — точное решение примера 2.2."""
    y = 2 * exp(t ** 2 / 2) - 1
    y1 = 2 * t * exp(t ** 2 / 2)
    return y, y1

# ============================================================
# ОДУ 2-го порядка (вар. 12)
#   y'' = - 4y
# ============================================================


def data_ode():
    """t0, y(t0), y'(t0)."""
    t0 = 0.0
    y0 = 0.0
    y1 = 2.0
    return t0, y0, y1


def ode_rhs(t, y, yp):
    """y'' = -4y."""
    return -4*y


def analytical_ode(t):
    """y(t), y'(t) — точное решение примера вар.12."""
    y = sin(2*t)
    y1 = 2*cos(2*t)
    return y, y1