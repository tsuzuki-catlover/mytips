import numpy as np


def is_monotone(equation, xmin, xmax, nsegment=100):
    x = np.linspace(xmin, xmax, nsegment)
    y = equation(x)

    dy = y[1:] - np.roll(y, 1)[1:]
    if np.all(dy >= 0):
        status = 1
    elif np.all(dy <= 0):
        status = -1
    else:
        status = 0

    return status


def cross_zero(equation, xmin, xmax):
    if equation(xmin) * equation(xmax) < 0:
        return True
    else:
        return False


def bisection(equation, xmin, xmax, epsilon=1e-8, max_iteration=1000):
    # Check monotonicity
    assert not is_monotone(equation, xmin, xmax) == 0,\
        'This function is not monotonic within the defined range.'

    # Check, if the function crosses zero
    assert cross_zero(equation, xmin, xmax),\
        'No answer is expected in the region defined.'

    x0 = xmin
    x1 = xmax
    n_iteration = 0
    while True:
        x2 = (x0 + x1) * 0.5
        if cross_zero(equation, x0, x2):
            x1 = x2
        else:
            x0 = x2

        if abs(equation(x2)) < epsilon or n_iteration > max_iteration:
            break

    return x2


def equation(x):
    # Put an equation
    return x**2 - 100


if __name__ == '__main__':
    xmin = 0
    xmax = 50
    ans = bisection(equation, xmin, xmax)
    print(ans)
