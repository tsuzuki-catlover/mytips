from pathlib import Path

import cv2
import numpy as np


def imread(filename, flags=cv2.IMREAD_COLOR):
    """imread for path containing Japanese character."""
    try:
        n = np.fromfile(filename, dtype=np.uint8)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return False


def imwrite(filename, img, params=None):
    """imwrite for path containing Japanese characters."""
    try:
        ext = Path(filename).suffix
        res, n = cv2.imencode(ext, img, params)
        if res:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    a = imread('ぬこ.png')
    imwrite('ぬこ２.jpg', a)
