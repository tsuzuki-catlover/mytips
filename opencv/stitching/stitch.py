import argparse
import sys

import cv2
import numpy as np


def matcher(img1, img2, draw=False):
    # Detect Features and Keypoints
    akaze = cv2.AKAZE_create()

    kp1 = akaze.detect(img1, None)
    kp2 = akaze.detect(img2, None)

    kp1, des1 = akaze.compute(img1, kp1)
    kp2, des2 = akaze.compute(img2, kp2)

    # print('{} features found in image1'.format(len(kp1)))
    # print('{} features found in image2'.format(len(kp2)))

    # Find matching
    FLANN_INDEX_LSH = 6
    index_params = dict(algorithm=FLANN_INDEX_LSH,
                        table_number=6,
                        key_size=12,
                        multi_probe_level=1)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    matchesMask = [[0, 0] for i in range(len(matches))]

    good = []
    for i, m in enumerate(matches):
        if len(m) < 2:
            continue
        if m[0].distance < 0.3 * m[1].distance:
            matchesMask[i] = [1, 0]
            good.append(m[0])

    # print('{} features matched'.format(len(good)))

    if draw:
        draw_params = dict(matchColor=(0, 255, 0),
                           singlePointColor=(0, 0, 255),
                           matchesMask=matchesMask,
                           flags=0)

        img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, matches, None,
                                  **draw_params)
        cv2.imwrite('matching.bmp', img3)

    return kp1, kp2, good


def homography_matrix(kp1, kp2, matches):
    pts1 = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    pts2 = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

    homography, mask = cv2.findHomography(pts2, pts1, cv2.RANSAC, 5.0)

    return homography


def get_dimension(w1, h1, w2, h2, H):
    # Calculate size and offset of the merged panorama
    pts = np.array([[0, w2, w2, 0], [0, 0, h2, h2], [1, 1, 1, 1]])
    pts_prime = np.dot(H, pts)
    pts_prime = pts_prime / pts_prime[2]

    # Get width: right edge - left edge
    stitched_w = \
        int(max(pts_prime[0, 1], pts_prime[0, 2], w1)) - \
        int(min(pts_prime[0, 0], pts_prime[0, 3], 0))
    # Get height: bottom edge - top edge
    stitched_h = \
        np.max(np.int32(pts_prime / pts_prime[2])[1]) - \
        np.min(np.int32(pts_prime / pts_prime[2])[1], 0)
    stitched = [stitched_w, stitched_h]

    offset = [
        -int(min(pts_prime[0, 0], pts_prime[0, 3], 0)),
        -int(min(pts_prime[1, 0], pts_prime[1, 1], 0))
    ]

    wrap = np.matrix([[1., 0., offset[0]], [0., 1., offset[1]], [0., 0., 1.]])

    T = wrap * H
    # print('Transform matrix')
    # print(T)

    # print('original size:', w1, h1)
    # print('stitched size:', stitched_w, stitched_h)
    # print('offset:       ', offset[0], offset[1])

    return stitched, offset, T


def stitcher(img1, img2, outname):
    """Stitch 2 images into 1 image.
    img1: first image
    img2: second image
    outname: path to the stitched image
    """
    # Shapes
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]

    # Get keypoints
    kp1, kp2, matches = matcher(img1, img2)

    # Calculate Homography
    homography = homography_matrix(kp1, kp2, matches)

    # Offset and size
    size, offset, translation = get_dimension(w1, h1, w2, h2, homography)

    # Merge the images
    panorama = np.zeros((size[1], size[0], 3), np.uint8)
    cv2.warpPerspective(img2, translation, size, panorama)
    panorama[offset[1]:offset[1] + h1, offset[0]:offset[0] + w1] = img1

    cv2.imwrite(outname, panorama)


if __name__ == '__main__':
    # Load images
    img1 = cv2.imread(sys.argv[1])
    img2 = cv2.imread(sys.argv[2])
    outname = sys.argv[3]

    stitcher(img1, img2, outname)
