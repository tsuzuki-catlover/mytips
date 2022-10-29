import numpy as np


def trapezoid(xmin, xmax, epsilon=1e-4):
    x = np.arange(xmin, xmax + epsilon, epsilon)
    y = equation(x)
    sum = np.sum((y[1:] + y[:-1])) * epsilon * 0.5

    return sum


def equation(x):
    return x**3


if __name__ == '__main__':
    xmin = 1
    xmax = 2
    ans = trapezoid(xmin, xmax)
    print(ans)
