import cv2
import numpy as np
import time
from statistics import mean
cap = cv2.VideoCapture('./images/TEST.mp4')
bg = cv2.imread('./images/background.jpg')
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
flag = False
prev_frame_time = 0
new_frame_time = 0
fps_list = []
while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.resize(frame, (720, 480))
    if not ret:
        break
    h = frame.shape[0]
    w = frame.shape[1]
    if flag == False:
        bg = cv2.resize(bg, (w, h))
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (3,3), 1)
    thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 13, 5)
    
    # ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    canny = cv2.Canny(img, 9, 0, True)
    edges = preprocessing(canny)

    cnt = sorted(cv2.findContours(edges, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)[-2], key=cv2.contourArea)[-1]

    mask = np.zeros((h, w), np.uint8)
    masked = cv2.drawContours(mask, [cnt], -1, 255, -1)
    kernel = np.ones((50,50), np.uint8)
    kernel_1 = np.ones((2,2), np.uint8)
    masked = cv2.erode(masked, kernel, iterations = 1)
    masked = cv2.erode(masked, kernel_1, iterations = 3)
    dst_fg = cv2.bitwise_and(frame, frame, mask=masked)
    mask_inversed = cv2.bitwise_not(masked)
    dst_bg = cv2.bitwise_and(bg, bg, mask=mask_inversed)
    dst = cv2.bitwise_or(dst_fg, dst_bg)
    new_frame_time = time.time()
    fps = 1/(new_frame_time - prev_frame_time)
    fps_list.append(fps)
    prev_frame_time = new_frame_time
    print(max(fps_list))
    
    cv2.imshow('frame', dst_fg)
    if cv2.waitKey(25) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
