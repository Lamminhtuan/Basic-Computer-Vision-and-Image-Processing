import cv2
import imageio
import numpy as np
mask = cv2.imread('images/tiger_mask.png')
cv2.imshow('view',mask)
cv2.waitKey(0)
