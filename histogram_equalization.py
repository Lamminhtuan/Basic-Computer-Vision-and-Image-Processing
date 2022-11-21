import cv2 
import numpy as np
import matplotlib.pyplot as plt
img = cv2.imread('images/lowcontrast.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#calculate the histogram
def df(img):
    values = np.zeros([256], np.uint32)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            values[img[i][j]] += 1
    return values
#calculate the cdf and h(v)
def hv(hist):
    cdf = np.zeros(len(hist))
    cdf[0] = hist[0] 
    for i in range(1, len(hist)):
        cdf[i] = cdf[i-1] + hist[i]
    #formula
    cdf = np.around((cdf - cdf.min()) / (cdf[-1] - cdf.min()) * 255)
    return cdf
#equalize
def equalize(img):
    img_eq = np.zeros((img.shape[0], img.shape[1]))
    mapping = hv(df(img))
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            #mapping...
            img_eq[i][j] = mapping[img[i][j]]
    return img_eq.astype(np.uint8)
result = equalize(img)
cv2.imshow('Equalized', result)
cv2.waitKey(0)
