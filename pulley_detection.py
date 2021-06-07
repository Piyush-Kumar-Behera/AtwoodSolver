import numpy as np
import cv2

def get_pulley(img, contour):
    max_area = -1
    max_area_idx = -1
    for i in range(len(contour)):
        c = contour[i]
        if c[0][0][0] != -1:
            c_area = cv2.contourArea(c)
            if c_area > max_area:
                max_area = c_area
                max_area_idx = i
    selected_contour = cv2.convexHull(contour[max_area_idx])
    contour[max_area_idx] = [[[-1, -1]]]

    return contour, selected_contour

if __name__ == '__main__':
    pass