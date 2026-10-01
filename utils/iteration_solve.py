from numpy import arange


def solve(a, b, h, x_0, y_0, x_next, y_next):

    t = arange(a, b + h, h)
    x, y = [x_0], [y_0]

    for i in range(len(t) - 1):
        x.append(x_next(x[i], y[i], t[i]))
        y.append(y_next(x[i], y[i], t[i]))

    return x, y, t