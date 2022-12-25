import cv2
import numpy as np
ori = cv2.imread('./images/tiger.jpg')
bg = cv2.imread('./images/background.jpg')

h = ori.shape[0]
w = ori.shape[1]
#Convert to grayscale
bg = cv2.resize(bg, (w, h))

img = cv2.cvtColor(ori, cv2.COLOR_BGR2GRAY)
# img = cv2.add(img, 10)
#Binarizing
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
    
    edges = cv2.dilate(image, kernel, iterations = 1)
    # edges = cv2.erode(edges, kernel, iterations = 1)
    # edges = cv2.dilate(edges, kernel_1, iterations = 1)
    # edges = cv2.erode(edges, kernel_1, iterations = 1)
    # edges = cv2.dilate(edges, kernel_3, iterations = 1)
    # edges = cv2.erode(edges, kernel_3, iterations = 1)
    # edges = cv2.dilate(edges, kernel_2, iterations = 1)
    # edges = cv2.erode(edges, kernel_2, iterations = 1)
    return edges
img = cv2.GaussianBlur(img, (3,3), 0)
# thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
#             cv2.THRESH_BINARY_INV,9, 3)
canny = auto_canny(img)
ret,thresh = cv2.threshold(canny,156,255,cv2.THRESH_BINARY)

edges = preprocessing(thresh)
# edges = cv2.dilate(edges, kernel_1, iterations = 1)
# edges = cv2.erode(edges, kernel_1, iterations = 1)
cnt = sorted(cv2.findContours(edges, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)[-2], key=cv2.contourArea)[-1]
# contours, _ = cv2.findContours(edges, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
mask = np.zeros((h, w), np.uint8)
kernel = np.ones((5,5), np.uint8)
masked = cv2.drawContours(mask, [cnt], -1, 255, -1)
masked = cv2.erode(masked, kernel, iterations = 2)
# masked = preprocessing(masked)
# con = cv2.drawContours(ori, [cnt], -1, (255,0,0), 5)
# masked = cv2.GaussianBlur(masked, (5, 5), 0)
dst_fg = cv2.bitwise_and(ori, ori, mask=masked)
mask_inversed = cv2.bitwise_not(masked)
dst_bg = cv2.bitwise_and(bg, bg, mask=mask_inversed)
dst = cv2.bitwise_or(dst_fg, dst_bg)
cv2.imshow('Ori', masked)
cv2.imshow('Result', dst_fg)
cv2.waitKey(0)
