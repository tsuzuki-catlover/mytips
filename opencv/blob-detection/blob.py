import cv2
import numpy as np


def contour_defect(source, annotation):
    """Blob detections."""
    params = cv2.SimpleBlobDetector_Params()

    # Just area criteria
    params.filterByArea = True
    params.minArea = 1
    params.maxArea = 50000
    params.filterByCircularity = False
    params.filterByConvexity = False
    params.filterByInertia = False
    params.filterByColor = False

    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(annotation)

    blank = np.zeros((1, 1))
    results = cv2.drawKeypoints(source, keypoints, blank, (0, 255, 0),
                                cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    return results
