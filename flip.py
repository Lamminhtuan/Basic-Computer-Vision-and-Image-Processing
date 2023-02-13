import cv2
import numpy as np

img = cv2.imread('./Irelia_6.jpg')

img_light = cv2.add(img, 100)

#img_flip_ver = cv2.flip(img, 0) 
img_flip_ver = img[:,::-1]
#img_flip_hr = cv2.flip(img, 1)
img_flip_hr = img[::-1,:]
img_neg = 255 - img
cv2.imshow('Image light', img_light)
cv2.imshow('Image flip vertically', img_flip_ver)
cv2.imshow('Image flip horizontally', img_flip_hr)
cv2.imshow('Negative image', img_neg)
cv2.waitKey(0)