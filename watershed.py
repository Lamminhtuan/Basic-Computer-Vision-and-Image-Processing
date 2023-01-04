import cv2
import numpy as np
ori = cv2.imread('./images/ws.jpg')
blur = cv2.GaussianBlur(ori, (5, 5), 0)
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# thresh = cv2.adaptiveThreshold(gray, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
#             cv2.THRESH_BINARY,107,2)
kernel = np.ones((3,3), np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations = 2)
sure_bg = cv2.dilate(opening, kernel, iterations = 2)
dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
ret, sure_fg = cv2.threshold(dist_transform,0.3*dist_transform.max(),255,0)
sure_fg = np.uint8(sure_fg)
unknown = np.subtract(sure_bg, sure_fg)
ret, markers = cv2.connectedComponents(sure_fg)
print(markers)
3.	## Add one so that sure background is not 1
markers = markers +1
5.	## Making the unknown area as 0
markers[unknown == 255] = 0
markers = cv2.watershed(ori, markers)
ori[markers == -1] = (255, 0, 0)
cv2.imshow('result', ori)
cv2.waitKey(0)
