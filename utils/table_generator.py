import numpy as np
import pandas as pd
from tabulate import tabulate

from utils.calculation_error import max_error_percent


def fmt(v):
    if v == 0:
        return "0"
    return (f"{v:.5f}".rstrip('0').rstrip('.')
            if int(abs(v) * 1e5) % 10
            else f"{v:.2e}")


def fmt_array(a):
    a = np.asarray(a, dtype=float)
    return np.array([fmt(v) for v in a.ravel()], dtype=object).reshape(a.shape)


def generate_table_for_decisions(x, y, x_approx, y_approx, t, step=1):
    """
    Генерация и вывод таблицы сравнения точного и приближённого решений

    Параметры:
    x, y - точные решения
    x_approx, y_approx - приближённые решения
    t - массив времени
    step - шаг выборки (выводим каждую step-ю строку)
    """
    if step < 1:
        step = 1

    # Преобразуем все данные в массивы NumPy
    x = np.array(x)
    y = np.array(y)
    x_approx = np.array(x_approx)
    y_approx = np.array(y_approx)
    t = np.array(t)

    # Создаём индексы для выборки
    indices = np.arange(0, len(t), step, dtype=int)

    # Выбираем данные с заданным шагом
    t_selected = t[indices]
    x_selected = x[indices]
    y_selected = y[indices]
    x_approx_selected = x_approx[indices]
    y_approx_selected = y_approx[indices]

    # Создаём словарь с данными
    data = {
        't': t_selected,
        'x': x_selected,
        'y': y_selected,
        'x_T': x_approx_selected,
        'y_T': y_approx_selected,
        'Δx': np.abs(x_selected - x_approx_selected),
        'Δy': np.abs(y_selected - y_approx_selected)
    }

    data = {k: fmt_array(arr) for k, arr in data.items()}
    # Создаём DataFrame
    df = pd.DataFrame(data)

    # Округляем до 6 знаков
    df = df.round(6)

    # Настройка отображения pandas
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.float_format', '{:.6f}'.format)

    return tabulate(df, headers='keys', tablefmt='grid', showindex=False), len(df), step


def generate_table_for_error(x, y, x_approx_dict, y_approx_dict, h):
    """
    Генерация сводной таблицы погрешностей для одного шага
    """
    x = np.array(x)
    y = np.array(y)
    methods = list(x_approx_dict.keys())

    table_data = []
    table_data.append([f'Шаг {h}'] + [''] * len(methods))

    for error_type in ['δx', 'δy']:
        row = [error_type]
        for method in methods:
            x_approx = np.array(x_approx_dict[method])
            y_approx = np.array(y_approx_dict[method])

            if error_type == 'δx':
                # Вычисляем относительную погрешность в цикле
                rel_errors = []
                for i in range(len(x)):
                    if abs(x[i]) > 1e-10:
                        rel_errors.append(abs(x[i] - x_approx[i]) / abs(x[i]) * 100)
                mean_rel_err = np.mean(rel_errors)
            else:
                rel_errors = []
                for i in range(len(y)):
                    if abs(y[i]) > 1e-10:
                        rel_errors.append(abs(y[i] - y_approx[i]) / abs(y[i]) * 100)
                mean_rel_err = np.mean(rel_errors)

            row.append(f'{mean_rel_err:.4f}')

        table_data.append(row)

    headers = ['δ, %'] + methods
    return tabulate(table_data, headers=headers, tablefmt='grid', floatfmt='.4f')


# def generate_table_for_error(x, y, x_approx_dict, y_approx_dict, h, methods, error_type):
#     """
#     Генерация сводной таблицы погрешностей для одного шага
#
#     Параметры:
#         x, y - точные значения
#         x_approx_dict, y_approx_dict - словари с приближёнными значениями по методам
#         h - шаг
#         methods - список методов
#         error_type - функция для вычисления погрешности в точке
#     """
#     x = np.array(x)
#     y = np.array(y)
#
#     table_data = []
#     table_data.append([f'Шаг {h}'])
#
#     for err_label in ['δx', 'δy']:
#         row = [err_label]
#         for method in methods:
#             x_approx = np.array(x_approx_dict[method])
#             y_approx = np.array(y_approx_dict[method])
#
#             if err_label == 'δx':
#                 mean_rel_err = max_error_percent(x, x_approx, error_type)
#             else:
#                 mean_rel_err = max_error_percent(y, y_approx, error_type)
#
#             row.append(f'{mean_rel_err:.4f}')
#
#         table_data.append(row)
#
#     headers = ['δ, %'] + methods
#     return tabulate(table_data, headers=headers, tablefmt='grid', floatfmt='.4f')


def additional_information(generated_table):
    string_table, length, step = generated_table[0], generated_table[1], generated_table[2]
    # Дополнительная информация
    return f"\nВсего строк в таблице: {length} (выбрано с шагом {step})"


def print_table(x, y, x_approx, y_approx, t, step=10):
    print(generate_table_for_decisions(x, y, x_approx, y_approx, t, step)[0])
