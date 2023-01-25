import cv2
import numpy as np
import time
from statistics import mean
#Đường dẫn chứa file test
cap = cv2.VideoCapture('./images/test.mp4')
def auto_canny(image, sigma = 0.33):
    v = np.median(image)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper, True)
    return edged
def preprocessing(image):
    kernel_dil = np.ones((50,50), np.uint8)
    edges = cv2.dilate(image, kernel_dil, iterations = 1)
    return edges
size = (1280, 720)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, size)
    h = frame.shape[0]
    w = frame.shape[1]
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (3,3), 1)
    thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 13, 5)
    canny = cv2.Canny(img, 9, 0, True)
    edges = preprocessing(canny)
    contours = cv2.findContours(edges, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)[-2]
    #Nếu tìm được đường viền
    if contours:
        #Lấy đường viền lớn nhất
        cnt = max(contours, key=cv2.contourArea)
        mask = np.zeros((h, w), np.uint8)
        masked = cv2.drawContours(mask, [cnt], -1, 255, -1)
        kernel = np.ones((50,50), np.uint8)
        kernel_1 = np.ones((2,2), np.uint8)
        masked = cv2.erode(masked, kernel, iterations = 1)
        masked = cv2.erode(masked, kernel_1, iterations = 3)
        dst_fg = cv2.bitwise_and(frame, frame, mask=masked)
        cv2.imshow('frame', dst_fg)
    else:
        cv2.imshow('frame', frame)
    if cv2.waitKey(25) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
print('Hết video')
