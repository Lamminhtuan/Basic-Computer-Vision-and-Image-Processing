import cv2
import numpy as np
ori = cv2.imread('./images/cf.jpg')
h = ori.shape[0]
w = ori.shape[1]
#Convert to grayscale
img = cv2.cvtColor(ori, cv2.COLOR_BGR2GRAY)
# img = cv2.add(img, 10)
#Binarizing
kernel = np.ones((1,1), np.uint8)
kernel_dil = np.ones((3,3), np.uint8)
img = cv2.GaussianBlur(img, (3,3), 0)
canny = cv2.Canny(img, 10, 100)
# ret, thresh = cv2.threshold(img, np.mean(img), 255, cv2.THRESH_BINARY_INV)
# edges = cv2.erode(canny, kernel, iterations = 1)
edges = cv2.dilate(canny, kernel_dil, iterations = 1)
cnt = sorted(cv2.findContours(edges, mode=cv2.RETR_CCOMPF, method=cv2.CHAIN_APPROX_SIMPLE)[-2], key=cv2.contourArea)[-1]
# contours, _ = cv2.findContours(edges, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
mask = np.zeros((h, w), np.uint8)
masked = cv2.drawContours(mask, [cnt], -1, 255, -1)
dst = cv2.bitwise_and(ori, ori, mask=mask)
cv2.imshow('Mask', canny)
cv2.imshow('Result', dst)
cv2.waitKey(0)
