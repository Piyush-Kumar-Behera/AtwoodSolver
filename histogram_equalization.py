import numpy as np
import cv2
import matplotlib.pyplot as plt
def equalizeHistogram(image, max_hist_val = 200):
    '''
    Input: 
    image: Grayscale input image
    max_hist_val: The maximum value of pixel intesity to be considered by histogram, to compensate for the domination of 
                  higher intensity value(white background)

    Output: The returned image's pixel distribution upto max_hist_val pixel is equalized 
    '''
    hist, bins = np.histogram(image.flatten(), max_hist_val, [0,max_hist_val])

    cdf = hist.cumsum()
    cdf_normalized = cdf * float(hist.max()) / cdf.max()

    cdf_m = np.ma.masked_equal(cdf,0)
    cdf_m = (cdf_m - cdf_m.min())*max_hist_val/(cdf_m.max()-cdf_m.min())
    cdf = np.ma.filled(cdf_m,0).astype('uint8')

    white_ar = 255 * np.ones((256-max_hist_val,)) 
    white_ar = white_ar.astype('uint8')

    cdf = np.append(cdf, white_ar)
    img_ret = cdf[image]
    # print(cdf)
    # print(cdf.shape)

    return img_ret

if __name__ == '__main__':
    image_loc = 'images/Pulley_Ex2.png'
    img = cv2.imread(image_loc)
    median_blur = cv2.medianBlur(img, 11)
    gray_mb = cv2.cvtColor(median_blur, cv2.COLOR_BGR2GRAY)

    custom = equalizeHistogram(gray_mb)
    inbuilt = cv2.equalizeHist(gray_mb)

    cv2.imshow('Orig', gray_mb)
    cv2.imshow('Custom', custom)
    cv2.imshow('Inbuilt', inbuilt)
    cv2.waitKey(0)
    cv2.destroyAllWindows()