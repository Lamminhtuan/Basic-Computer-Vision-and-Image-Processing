import cv2
import numpy as np

def process(img, b_k, b_s, c_t1, c_t2, k1, k2, k3, k4, iter1, iter2):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    b_k = b_k // 2 * 2 + 1
    img_blur = cv2.GaussianBlur(img_gray, (b_k, b_k), b_s)
    img_canny = cv2.Canny(img_blur, c_t1, c_t2)
    img_dilate = cv2.dilate(img_canny, np.ones((k1, k2)), iterations=iter1)
    img_erode = cv2.erode(img_dilate, np.ones((k3, k4)), iterations=iter2)
    return cv2.bitwise_not(img_erode)
d = {"Blue Kernel": (3, 50), 
"Blur Sigma": (2, 30),
"Canny Threshold 1":(50, 500),
"Canny Threshold 2": (9,500),
"Dilate Kernel 1": (4, 50),
"Dilate Kernel 2": (2, 50), 
"Erode Kernel 1": (13, 50),
"Erode Kernel 2": (7, 50),
"Dilate Interations": (11, 40),
"Erode Iterations": (4,40)
}
cv2.namedWindow("Track Bars")
for i in d:
    cv2.createTrackbar(i, "Track Bars", *d[i], id)
img = cv2.imread('images/g63.jpg')
while True:
    img_copy = img.copy()
    processed = process(img, *(cv2.getTrackbarPos(i, "Track Bars") for i in d))
    contours, _ = cv2.findContours(processed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        cnt = max(contours, key=cv2.contourArea)
        cv2.drawContours(img_copy, [cnt], -1, 255, 1)
    cv2.imshow('result', img_copy)
    if cv2.waitKey(1) == ord('q'): break
cv2.waitKey(0)
cv2.destroyAllWindows()