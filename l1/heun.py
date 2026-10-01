from data.option import f_1, f_2


def formula(h):
    x_next = lambda x_i, y_i, t_i: x_i + h * (0.5 * f_1(t_i, y_i) + 0.5 * f_1(t_i + h, y_i + h * f_2(t_i, x_i)))
    y_next = lambda x_i, y_i, t_i: y_i + h * (0.5 * f_2(t_i, x_i) + 0.5 * f_2(t_i + h, x_i + h * f_1(t_i, y_i)))

    return x_next, y_next
