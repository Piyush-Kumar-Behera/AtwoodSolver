import numpy as np
import cv2
import math

def point_dist(p1 = None, p2 = None):
    return math.sqrt(abs(p1[0]-p2[0])**2 + abs(p1[1]-p2[1])**2)

def remove_background(img = None, hierarchy = None, contour = None):
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    m, n = img.shape

    bg_dist = m*n
    bg_contour_pos = -1

    check_points = np.asarray([(m,n),(m,0),(0,n),(0,0)])
    for i in range(len(contour)):
        c = contour[i]
        cp_dist = []

        for cp in check_points:
            min_dist = m*n

            for p in c:
                p_d = point_dist(p[0],cp)
                if p_d < min_dist:
                    min_dist = p_d

            cp_dist.append(min_dist)

        sum_cp_dist = np.sum(cp_dist)
        if sum_cp_dist < bg_dist:
            bg_dist = sum_cp_dist
            bg_contour_pos = i


    contour[bg_contour_pos] = [[[-1,-1]]]

    return contour, hierarchy


def remove_small_area(img = None, hierarchy = None, contour = None, min_area = 500):
    remove_list = []
    for i in range(len(contour)):
        if contour[i][0][0][0] != -1:
            if cv2.contourArea(contour[i]) < min_area:
                remove_list.append(i)

    for idx in remove_list:
        contour[idx] = [[[-1,-1]]]
    return contour, hierarchy


def count_child(contour = None, hierarchy = None, idx = None):
    count = 1
    if hierarchy[0][idx][0] != -1:
        count += count_child(contour, hierarchy, hierarchy[0][idx][0])
    if hierarchy[0][idx][2] != -1:
        count += count_child(contour, hierarchy, hierarchy[0][idx][2])
    
    return count

def remove_outer_contour(img = None, hierarchy = None, contour = None, max_contain = 2):
    remove_list = []
    for i in range(len(contour)):
        if contour[i][0][0][0] != -1:
            j = hierarchy[0][i][2]
            if j != -1:
                count = count_child(contour, hierarchy, j)
                if count > max_contain:
                    remove_list.append(i)
    
    for idx in remove_list:
        contour[idx] = [[[-1,-1]]]
    return contour, hierarchy

if __name__ == '__main__':
    pass         