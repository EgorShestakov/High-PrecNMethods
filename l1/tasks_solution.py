from data.option import data, analytical_decision
import Euler as Eu
import Heun as He
from utils.build_graph import build_option_graph
from utils.iteration_solve import solve
from utils.table_generator import print_table, generate_table_for_error


def method_solve(data, h, formula):
    a, b, x0, y0 = data()
    x_next_formula, y_next_formula = formula
    x, y, t = solve(a, b, h, x0, y0, x_next_formula, y_next_formula)

    return x, y, t


def solve_several_h():
    for i in range(1, 4):
        h = 10**(-i)

        x_euler, y_euler, t = method_solve(data, h, Eu.formula(h))
        x_heun, y_heun, t = method_solve(data, h, He.formula(h))
        x, y = analytical_decision(t)
        print_table(x, y, x_euler, y_euler, t, step=10)
        print_table(x, y, x_heun, y_heun, t, step=10)
        print(generate_table_for_error(x, y, {'Метод Эйлера': x_euler, 'Метод Хойна': x_heun},
            {'Метод Эйлера': y_euler, 'Метод Хойна': y_heun}, h))
        build_option_graph(x, y, x_euler, y_euler, t, h, "Эйлера")
        build_option_graph(x, y, x_heun, y_heun, t, h, "Хойна")


if __name__ == "__main__":
    solve_several_h()