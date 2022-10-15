import cv2
import numpy as np
a = cv2.imread('images/9-ro-dark.jpeg')
def normalize_image(input):
    input[:,:,0] = 255 * ((input[:,:,0] - input[:,:,0].min()) / (input[:,:,0].max() - input[:,:,0].min()))
    input[:,:,1] = 255 * ((input[:,:,1] - input[:,:,1].min()) / (input[:,:,1].max() - input[:,:,1].min()))
    input[:,:,2] = 255 * ((input[:,:,2] - input[:,:,2].min()) / (input[:,:,2].max() - input[:,:,2].min()))
    return input
a = normalize_image(a)
print(a.max())
cv2.imshow('view', a)
cv2.waitKey(5000)