import numpy as np
import cv2

def contour_width(img, contour):
    x_limit = img.shape[1]
    max_x = -1
    min_x = x_limit+1

    for points in contour:
        x = points[0][0]
        if x < min_x:
            min_x = x
        if x > max_x:
            max_x = x

    diff = abs(max_x-min_x)
    return diff/x_limit

    
def get_wedge(img = None, contour = None, area_ratio = 0.3, dim_ratio = 0.5, strict_check = False):
    img_area = img.shape[0]*img.shape[1]
    approx = None
    for i in range(len(contour)):
        flag1 = 0
        flag2 = 0
        c = contour[i]
        if c[0][0][0] != -1:
            area = cv2.contourArea(c)
            width = contour_width(img, c)
            if area/img_area > 0.5:
                flag1 = 1

            if width > 0.3:
                flag2 = 1
        
            if (flag1+flag2 >= 1 and strict_check == False) or (flag1+flag2 >= 2 and strict_check == True):
                contour[i] = [[[-1,-1]]]
                epsilon = 0.01*cv2.arcLength(c,True)
                approx = cv2.approxPolyDP(c,epsilon,True)

    return contour, approx  
    
if __name__ == '__main__':
    pass