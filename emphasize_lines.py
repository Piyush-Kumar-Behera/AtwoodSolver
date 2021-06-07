import cv2
import numpy as np

def count_pix(ar = None, baseline = 0.01):
    m, n = ar.shape

    count_ret = 0
    for i in range(m):
        for j in range(n):
            if ar[i][j] > baseline:
                count_ret += 1

    return count_ret

def emphasize_white(img = None, filter_size = (3,3), num_pixels = None):
    if num_pixels is None:
        num_pixels = 1

    ret, thresh = cv2.threshold(img, 127, 255, 0)
    thresh_norm = thresh/255.0
    f1, f2 = filter_size
    m, n = thresh.shape
    # print(thresh.shape)
    for i in range(m-(f1-1)):
        for j in range(n-(f2-1)):
            count = count_pix(thresh_norm[i:i+f1,j:j+f2])
            if count >= num_pixels:
                row = i+int((f1-1)/2)
                column = j+int((f2-1)/2)
                thresh[row,column] = 255

    return thresh

if __name__ == '__main__':
    pass