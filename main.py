import argparse 
import cv2
import numpy as np
from emphasize_lines import emphasize_white
from histogram_equalization import equalizeHistogram
from contour_selection import remove_background, remove_small_area, remove_outer_contour
from block_detection import get_blocks
from wedge_detection import get_wedge
from pulley_detection import get_pulley
from rope import rope
from block import block
from solve import solve_rope

ap = argparse.ArgumentParser()
ap.add_argument('-i','--image', type=str, required=False, help="Input image location")
args = vars(ap.parse_args())

for image_loc in ['images/Pulley_Ex2.png','images/Pulley_Ex3.png','images/Pulley_Ex4.png','images/Pulley_Ex5.png']:
    if args['image'] is not None:
        image_loc = args['image']

    img = cv2.imread(image_loc)

    #Median Blur to remove text and rope conecting blocks and pulleys
    median_blur = cv2.medianBlur(img, 11)
    gray_mb = cv2.cvtColor(median_blur, cv2.COLOR_BGR2GRAY)

    # OpenCV inbuilt Histogram Equalization
    # hist_equa = cv2.equalizeHist(gray_mb)

    # Custom Histogram Equalization 
    hist_equa = equalizeHistogram(gray_mb)

    # Canny Edge detector for edge detection
    mid = cv2.Canny(hist_equa, 10, 200)

    # Increasing width of the edges for continuous edges and better contour separation 
    thresh_emp = emphasize_white(mid, filter_size=(5,5))
    thresh_rev = 255-thresh_emp
    
    #-----------------Contour Extraction----------------------
    # Finding all contours in the image with a tree hierarchy
    contours, hierarchy = cv2.findContours(thresh_rev, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # remove contour representing the background
    contours, hierarchy = remove_background(img = thresh_rev, hierarchy=hierarchy, contour = contours)
    
    # remove small patches of contours
    contours, hierarchy = remove_small_area(img = thresh_rev, hierarchy=hierarchy, contour = contours)

    # removal of contours enclosing other contours in a parent-child hierarchy
    contours, hierarchy = remove_outer_contour(img = thresh_rev, hierarchy = hierarchy, contour = contours)


    #-----------------------Object Extraction---------------------
    # Module function call for block, wedge and pulley detection
    contours, blocks = get_blocks(img, contour=contours)
    contours, wedge = get_wedge(img=thresh_rev, contour = contours)
    pulley = get_pulley(img=img)


    #---------------------Solver---------------------
    # Creating string, block objects for solver 
    objects = dict()
    s1 = rope('s1', pulley[0], 'b1', 'b2')
    b1 = block('b1', 's1', (pulley[0][0],pulley[0][1]), blocks[0], m = 10)
    b2 = block('b2', 's1', (pulley[0][0],pulley[0][1]), blocks[1], m = 5)

    objects['s1'] = s1
    objects['b1'] = b1
    objects['b2'] = b2 

    objects = solve_rope('s1', objects = objects)
    print(s1.a, s1.T)
    


    # ----------------For representing the image------------- 
    img_copy = img
    cv2.rectangle(img_copy, (10,30), (200,70),(100,200,100), -1)
    cv2.putText(img_copy, 'Accelaration: '+str(abs(round(s1.a,2))) + ' m/s^2', (20,45), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,0,0), 1, cv2.LINE_AA)
    cv2.putText(img_copy, 'Tension: '+str(abs(round(s1.T,2)))+ ' N', (20,65), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,0,0), 1, cv2.LINE_AA)

    white_bg = np.ones(img.shape, dtype=np.uint8)*255
    
    if wedge is not None:
        cv2.drawContours(white_bg,[wedge],-1,(0,255,0),1)
        cv2.fillPoly(white_bg,pts = [wedge], color=(0,255,0))

    for i in range(len(blocks)):
        c = blocks[i]
        cv2.drawContours(white_bg,[c],-1,(0,0,255),1)
        cv2.fillPoly(white_bg,pts = [c], color=(0,0,255))
        # print(blocks[0])
    for p in pulley:
        cv2.circle(white_bg,(p[0],p[1]),p[2],(255,0,0),-1)

    cv2.imshow('Image_test',img_copy)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite('output_'+image_loc[:-4]+'_res_output.jpg', img_copy)

    if args['image'] is not None:
        break