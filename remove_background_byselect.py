import cv2
import numpy as np
cropping = False
img = cv2.imread('images/chromakey.jpg')
oriimage = img.copy()
oriiimage = img.copy()
def mouse_crop(event, x, y, flags, param):
    global x_start, y_start, x_end, y_end, cropping
    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping == True:
            x_end, y_end = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        x_end, y_end = x, y
        cropping = False
        refPoint = [(x_start, y_start), (x_end, y_end)]
        if len(refPoint) == 2: 
            roi = oriimage[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
            b, g, r = cv2.split(roi)
            min_b, max_b = b.min() - 30, b.max() + 27
            min_g, max_g = g.min() - 30, g.max() + 27
            min_r, max_r = r.min() - 30, r.max() + 27
            print(min_b, max_b, min_g, max_g, min_r, max_r)
            for i in range(0, oriiimage.shape[0]):
                for j in range(0, oriiimage.shape[1]):
                    
                    if oriiimage[i][j][0] > min_b and oriiimage[i][j][0] < max_b and oriiimage[i][j][1] > min_g and oriiimage[i][j][1] < max_g and oriiimage[i][j][2] > min_r and oriiimage[i][j][2] < max_r:
                        oriiimage[i][j][0] = 0
                        oriiimage[i][j][1] = 0
                        oriiimage[i][j][2] = 0
            cv2.imshow("background removed", oriiimage)
cv2.namedWindow("image")
cv2.setMouseCallback("image", mouse_crop)
#Crop vùng ảnh background để loại bỏ background
while True:
    i = img.copy()
    if not cropping:
        cv2.imshow("image", img)
    elif cropping:
        cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2)
        cv2.imshow("image", i)
        
    cv2.waitKey(1)
