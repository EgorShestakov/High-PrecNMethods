def abs_error(point_y, point_y_approx):
    """Абсолютная погрешность"""
    return abs(point_y - point_y_approx)


def rel_error(point_y, point_y_approx):
    """Относительная погрешность"""
    if point_y == 0:
        return float('inf')
    return abs_error(point_y, point_y_approx) / abs(point_y)


def calculate_error_in_points(y, y_approx, error_type):
    """Вычисляет погрешность для каждой точки"""
    if len(y) != len(y_approx):
        raise ValueError("Длины массивов должны совпадать")

    return [error_type(y[i], y_approx[i]) for i in range(len(y))]


def calculate_abs_and_rel_errors(y, y_approx):
    """Вычисляет абсолютную и относительную погрешности"""
    abs_errors = calculate_error_in_points(y, y_approx, abs_error)
    rel_errors = calculate_error_in_points(y, y_approx, rel_error)
    return abs_errors, rel_errors


def max_error_percent(y, y_approx, error_type):
    return max(calculate_error_in_points(y, y_approx, error_type)) * 100
