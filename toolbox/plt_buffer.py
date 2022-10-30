import io

import cv2
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt


def pyplot_to_numpy(fig: plt.figure) -> npt.NDArray[np.uint8]:
    """Convert matplotlib canvas into a Numpy array."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    buf.close()
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)

    return img


if __name__ == '__main__':
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111)
    x = np.linspace(-np.pi, np.pi)
    ax.plot(x, np.cos(x), color='r', ls='-', label='cos')
    ax.plot(x, np.sin(x), color='g', ls='-', label='sin')
    ax.plot(x, np.tan(x), color='b', ls='-', label='tan')

    ax.set_xlim(-np.pi, np.pi)
    ax.set_ylim(-2, 2)

    ax.legend()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.title.set_text('Trigonometry')

    img = pyplot_to_numpy(fig)

    cv2.imwrite('Trignometry.png', img)
