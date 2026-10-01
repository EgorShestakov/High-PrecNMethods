"""Лабораторная № 1. Методы Эйлера и Хойна."""

from data.option import analytical_decision, initial_condition, integration_interval
from utils.iteration_solve import solve
from utils.table_generator import print_table, generate_table_for_error
from utils.build_graph import build_option_graph

from l1 import euler as Eu
from l1 import heun as He


def method_solve(h, formula):
    t0, x0, y0 = initial_condition()
    t_start, t_end = integration_interval()
    x_next, y_next = formula
    x, y, t = solve(t_start, t_end, h, x0, y0, x_next, y_next)
    return x, y, t


def solve_several_h():
    for i in range(1, 4):
        h = 10 ** (-i)
        print(f"\n========== h = {h} ==========")

        x_e, y_e, t = method_solve(h, Eu.formula(h))
        x_h, y_h, _ = method_solve(h, He.formula(h))
        x, y = analytical_decision(t)

        print("\n--- Метод Эйлера ---")
        print_table(x, y, x_e, y_e, t, step=10)
        print(generate_table_for_error(
            x, y,
            {"Метод Эйлера": x_e},
            {"Метод Эйлера": y_e},
            h,
        ))
        build_option_graph(x, y, x_e, y_e, t, h, "Эйлера")

        print("\n--- Метод Хойна ---")
        print_table(x, y, x_h, y_h, t, step=10)
        print(generate_table_for_error(
            x, y,
            {"Метод Хойна": x_h},
            {"Метод Хойна": y_h},
            h,
        ))
        build_option_graph(x, y, x_h, y_h, t, h, "Хойна")


if __name__ == "__main__":
    solve_several_h()
