import numpy as np
import numpy.typing as npt


def trapezoid(xmin: float, xmax: float, epsilon: float = 1e-4) -> float:
    x = np.arange(xmin, xmax + epsilon, epsilon)
    y = equation(x)
    sum = np.sum((y[1:] + y[:-1])) * epsilon * 0.5

    return sum


def equation(x: npt.NDArray[np.float16]) -> npt.NDArray[np.float16]:
    return x**3


if __name__ == '__main__':
    xmin = 1
    xmax = 2
    ans = trapezoid(xmin, xmax)
    print(ans)
