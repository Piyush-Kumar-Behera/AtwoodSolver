import numpy as np
import cv2
from emphasize_lines import emphasize_white
from histogram_equalization import equalizeHistogram
from contour_selection import remove_background, remove_outer_contour, remove_small_area, point_dist

def block_hierarchy(b1, b2):
    res = True
    for point in b1:
        dist = cv2.pointPolygonTest(b2,(point[0],point[1]),False)
        if dist < 0:
            res = False
            break
    return res


def calculate_rect_area(rect_box = None):
    dist = []
    dist.append(point_dist(rect_box[0],rect_box[1]))
    dist.append(point_dist(rect_box[0],rect_box[3]))
    dist.append(point_dist(rect_box[0],rect_box[2]))
    dist = sorted(dist)

    return dist[0]*dist[1]

def detect_blocks(img = None, contour = None, epsilon = 0.1):
    rectangle_blocks = []
    for i in range(len(contour)):
        c = contour[i]
        if c[0][0][0] != -1:
            rect = cv2.minAreaRect(c)
            rect_box = np.int0(cv2.boxPoints(rect))
            cnt_area = cv2.contourArea(c)
            rect_area = calculate_rect_area(rect_box)

            if cnt_area/rect_area < (1+epsilon) and cnt_area/rect_area > (1-epsilon):
                rectangle_blocks.append(rect_box)
                contour[i] = [[[-1, -1]]]

    return contour, rectangle_blocks


def get_blocks(img = None, contour = None, epsilon = 0.1, redundant = False):
    contour, rectangle_blocks = detect_blocks(img,contour,epsilon)
    final_rect_blocks = None
    remove_list = []
    if redundant is False:
        for i in range(len(rectangle_blocks)):
            for j in range(len(rectangle_blocks)):
                if block_hierarchy(rectangle_blocks[i], rectangle_blocks[j]) and i != j:
                    remove_list.append(i)
    
    final_rect_blocks = [rectangle_blocks[i] for i in range(len(rectangle_blocks)) if i not in remove_list]

    return contour, final_rect_blocks

if __name__ == '__main__':
    image_loc = 'images/Pulley_Ex2.png'
    img = cv2.imread(image_loc)

    img = cv2.imread(image_loc)
    median_blur = cv2.medianBlur(img, 11)
    gray_mb = cv2.cvtColor(median_blur, cv2.COLOR_BGR2GRAY)

    hist_equa = equalizeHistogram(gray_mb)

    mid = cv2.Canny(hist_equa, 10, 200)
    thresh_emp = emphasize_white(mid, filter_size=(5,5))
    thresh_rev = 255-thresh_emp

    contours, hierarchy = cv2.findContours(thresh_rev, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = remove_background(img = thresh_rev, hierarchy=hierarchy, contour = contours)
    contours, hierarchy = remove_small_area(img = thresh_rev, hierarchy=hierarchy, contour = contours)

    contours, hierarchy = remove_outer_contour(img = thresh_rev, hierarchy = hierarchy, contour = contours)

    _, rectangle_blocks = get_blocks(img = img, contour=contours)

    