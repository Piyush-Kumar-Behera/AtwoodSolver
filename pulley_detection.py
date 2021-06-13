import numpy as np
import cv2

def get_pulley(img, param1 = 200, param2 = 12, minrad = 20, maxrad = 40):
    gray_2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.GaussianBlur(gray_2, (5,5),0)
    _, thresh_2 = cv2.threshold(gray_blur,200,255,cv2.THRESH_BINARY)
    pulley = []

    circles = cv2.HoughCircles(thresh_2, cv2.HOUGH_GRADIENT, 1, 20, param1 = param1, param2 = param2, minRadius = minrad, maxRadius = maxrad)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for pt in circles[0,:]:
            x,y,r = pt[0], pt[1], pt[2]
            pulley.append((x,y,r))
    
    return pulley