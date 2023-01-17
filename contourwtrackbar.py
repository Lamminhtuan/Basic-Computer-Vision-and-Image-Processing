import cv2
import numpy as np

def process(img, b_k, b_s, c_t1, c_t2, k1, k2, k3, k4, iter1, iter2):
    h, w = img.shape[:-1]
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    b_k = b_k * 2 + 1
    img_blur = cv2.GaussianBlur(img_gray, (b_k, b_k), b_s)
    img_canny = cv2.Canny(img_blur, c_t1, c_t2)
    img_dilate = cv2.dilate(img_canny, np.ones((k1, k2)), iterations=iter1)
    # img_erode = cv2.erode(img_dilate, np.ones((k3, k4)), iterations=iter2)
    contours, _ = cv2.findContours(img_dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    if contours:
        
        img_copy = img.copy()
        cnt = max(contours, key=cv2.contourArea)
        img_copy = cv2.drawContours(img_dilate, [cnt], -1, (255, 255, 0), 3)
        mask = np.zeros((h, w), np.uint8)

        masked = cv2.drawContours(mask, [cnt], -1, 255, -1)
        masked = cv2.erode(masked, np.ones((k3, k4)), iterations = iter2)
        dst_fg = cv2.bitwise_and(img, img, mask=masked)
        mask_inversed = cv2.bitwise_not(masked)
        # dst_bg = cv2.bitwise_and(bg, bg, mask=mask_inversed)
    
        return dst_fg
d = {"Blue Kernel": (3, 50), 
"Blur Sigma": (2, 30),
"Canny Threshold 1":(50, 500),
"Canny Threshold 2": (9,500),
"Dilate Kernel 1": (1, 50),
"Dilate Kernel 2": (1, 50), 
"Erode Kernel 1": (1, 50),
"Erode Kernel 2": (1, 50),
"Dilate Interations": (1, 40),
"Erode Iterations": (1,40)
}
cv2.namedWindow("Track Bars")
for i in d:
    cv2.createTrackbar(i, "Track Bars", *d[i], id)
img = cv2.imread('images/ori.jpg')

while True:
    img_copy = img.copy()   
    # print(*(cv2.getTrackbarPos(i, "Track Bars") for i in d))
    processed = process(img_copy, *(cv2.getTrackbarPos(i, "Track Bars") for i in d))
    
    cv2.imshow('result', processed)
    if cv2.waitKey(1) == ord('q'): break
cv2.waitKey(0)
cv2.destroyAllWindows()