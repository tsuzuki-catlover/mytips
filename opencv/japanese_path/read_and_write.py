from pathlib import Path

import cv2
import numpy as np
import numpy.typing as npt


def imread(filename: str, flags: int = cv2.IMREAD_COLOR) \
    -> npt.NDArray[np.uint8]:
    """imread for path containing Japanese character."""
    assert Path(filename).exists(), '{} does not exist!'.format(filename)

    img_arr = np.fromfile(filename, dtype=np.uint8)
    img = cv2.imdecode(img_arr, flags)

    return img


def imwrite(filename: str, img: npt.NDArray[np.uint8]) -> None:
    """imwrite for path containing Japanese characters."""
    try:
        _, img = cv2.imencode(Path(filename).suffix, img, None)
    except cv2.error:
        print('The image cannot be encoded into {}!'.format(filename))
        exit(1)

    with open(filename, mode='w+b') as f:
        img.tofile(f)


if __name__ == '__main__':
    a = imread('ぬこ.png')
    imwrite('ぬこ２.jpg', a)
