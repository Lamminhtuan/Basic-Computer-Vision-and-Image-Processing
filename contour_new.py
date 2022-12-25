import numpy as np
import cv2
ori = cv2.imread('./images/s1.jpg')

def auto_canny(image, sigma = 0.33):
    v = np.median(image)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
	# return the edged image
    return edged
def preprocessing(image):
    kernel = np.ones((5,5), np.uint8)
    kernel_dil = np.ones((5,5), np.uint8)
    kernel_1 = np.ones((1,1), np.uint8)
    kernel_2 = np.ones((5,5), np.uint8)
    kernel_3 = np.ones((3,3), np.uint8)
    
    edges = cv2.dilate(image, kernel, iterations = 3)
    # edges = cv2.erode(edges, kernel, iterations = 1)
    # edges = cv2.dilate(edges, kernel_1, iterations = 1)
    # edges = cv2.erode(edges, kernel_1, iterations = 1)
    # edges = cv2.dilate(edges, kernel_3, iterations = 1)
    # edges = cv2.erode(edges, kernel_3, iterations = 1)
    # edges = cv2.dilate(edges, kernel_2, iterations = 1)
    # edges = cv2.erode(edges, kernel_2, iterations = 1)
    return edges
h = ori.shape[0]
w = ori.shape[1]
blur = cv2.GaussianBlur(ori, (3, 3), 0)
img = cv2.cvtColor(ori, cv2.COLOR_BGR2GRAY)
edges = auto_canny(img)
ret, thresh = cv2.threshold(edges, 0 , 255, cv2.THRESH_BINARY)
thresh = preprocessing(edges)
cnt = sorted(cv2.findContours(thresh, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)[-2], key=cv2.contourArea)[-1]
# contours, _ = cv2.findContours(edges, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
mask = np.zeros((h, w), np.uint8)
masked = cv2.drawContours(mask, [cnt], -1, 255, -1)
kernel = np.ones((5,5), np.uint8)
kernel_1 = np.ones((5,5), np.uint8)
masked = cv2.erode(masked, kernel, iterations = 3)
masked = cv2.erode(masked, kernel_1, iterations = 1)
res = cv2.bitwise_and(ori, ori, mask=masked)
cv2.imshow('edges', edges)

cv2.imshow('result', res)
cv2.waitKey(0)