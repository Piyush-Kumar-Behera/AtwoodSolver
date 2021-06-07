import argparse 
import cv2
import numpy as np
from emphasize_lines import emphasize_white
from histogram_equalization import equalizeHistogram
from contour_selection import remove_background, remove_small_area, remove_outer_contour
from block_detection import get_blocks
from wedge_detection import get_wedge
from pulley_detection import get_pulley
ap = argparse.ArgumentParser()
ap.add_argument('-i','--image', type=str, required=False, help="Input image location")
args = vars(ap.parse_args())

for image_loc in ['images/Pulley_Ex1.png','images/Pulley_Ex2.png','images/Pulley_Ex3.png','images/Pulley_Ex4.png','images/Pulley_Ex5.png']:
    if args['image'] is not None:
        image_loc = args['image']

    img = cv2.imread(image_loc)
    median_blur = cv2.medianBlur(img, 11)
    gray_mb = cv2.cvtColor(median_blur, cv2.COLOR_BGR2GRAY)

    # OpenCV inbuilt Histogram Equalization
    # hist_equa = cv2.equalizeHist(gray_mb)

    # Custom Histogram Equalization 
    hist_equa = equalizeHistogram(gray_mb)

    mid = cv2.Canny(hist_equa, 10, 200)
    thresh_emp = emphasize_white(mid, filter_size=(5,5))
    thresh_rev = 255-thresh_emp

    contours, hierarchy = cv2.findContours(thresh_rev, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = remove_background(img = thresh_rev, hierarchy=hierarchy, contour = contours)
    contours, hierarchy = remove_small_area(img = thresh_rev, hierarchy=hierarchy, contour = contours)

    contours, hierarchy = remove_outer_contour(img = thresh_rev, hierarchy = hierarchy, contour = contours)

    contours, blocks = get_blocks(img, contour=contours)
    contours, wedge = get_wedge(img=thresh_rev, contour = contours)
    contours, pulley = get_pulley(img=thresh_rev,contour=contours)


    black_bg = np.zeros(img.shape, dtype=np.uint8)
    
    if wedge is not None:
        cv2.drawContours(black_bg,[wedge],-1,(0,255,0),1)
        cv2.fillPoly(black_bg,pts = [wedge], color=(0,255,0))

    for i in range(len(blocks)):
        c = blocks[i]
        cv2.drawContours(black_bg,[c],-1,(0,0,255),1)
        cv2.fillPoly(black_bg,pts = [c], color=(0,0,255))


    cv2.drawContours(black_bg,[pulley],-1,(255,0,0),1)
    cv2.fillPoly(black_bg,pts = [pulley], color=(255,0,0))
    cv2.imshow('Image_test',black_bg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite('output_'+image_loc[:-4]+'output.jpg', black_bg)
