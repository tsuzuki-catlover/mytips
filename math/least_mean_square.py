import numpy as np


def least_mean_square(data):
    copy_data = data.copy()
    copy_target = copy_data[:, 1].copy().reshape(-1, 1)
    copy_data[:, 1] = 1
    res = np.linalg.inv(copy_data.T @ copy_data) @ copy_data.T @ copy_target
    res = res.reshape(-1)

    return res


if __name__ == '__main__':
    x = np.array([[2.1, 4], [3, 5.9], [10, 19.8]])
    w = linear_fit(x)

    print(w)
