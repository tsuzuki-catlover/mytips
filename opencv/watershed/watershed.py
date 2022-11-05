import cv2
import numpy as np


def watershed(src,
              resize=1,
              blur=5,
              bin_thr=100,
              kernel=3,
              iter_morph=2,
              iter_sure=2,
              mask_size=3,
              dist_thr=0.05):
    img = cv2.imread(src)
    resize = max(min(resize, 1), 0)
    if resize == 0:
        resize = 1
    img = cv2.resize(img, dsize=None, fx=resize, fy=resize)
    blur = cv2.medianBlur(img, blur)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, bin_thr, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_CCOMP,
                                           cv2.CHAIN_APPROX_SIMPLE)
    filter_morph = np.ones((kernel, kernel), np.uint8)
    opening = cv2.morphologyEx(thresh,
                               cv2.MORPH_OPEN,
                               filter_morph,
                               iterations=iter_morph)
    sure_bg = cv2.dilate(opening, filter_morph, iterations=iter_sure)
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, mask_size)
    _, sure_fg = cv2.threshold(dist_transform, dist_thr * dist_transform.max(),
                               255, 0)
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0
    markers = cv2.watershed(img, markers)

    contours, hierarchy = cv2.findContours(markers.copy(), cv2.RETR_CCOMP,
                                           cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(contours)):
        if hierarchy[0][i][3] == -1:
            dst = cv2.drawContours(img, contours, i, (0, 255, 0), 1)

    return dst


if __name__ == '__main__':
    filename = 'riverside.jpg'
    watershed = watershed(filename)
    cv2.imshow('watershed', watershed)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
