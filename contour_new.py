import cv2
import numpy as np
cap = cv2.VideoCapture('./images/test.mp4')
bg = cv2.imread('./images/background.jpg')


#Convert to grayscale

def auto_canny(image, sigma = 0.33):
    v = np.median(image)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper, True)
    return edged
def preprocessing(image):
    kernel = np.ones((5,5), np.uint8)
    kernel_dil = np.ones((12,12), np.uint8)
    kernel_1 = np.ones((1,1), np.uint8)
    kernel_2 = np.ones((5,5), np.uint8)
    kernel_3 = np.ones((3,3), np.uint8)
    
    edges = cv2.dilate(image, kernel_dil, iterations = 1)
    # edges = cv2.erode(edges, kernel, iterations = 1)
    edges = cv2.dilate(edges, kernel_1, iterations = 5)
    # edges = cv2.erode(edges, kernel_1, iterations = 1)
    # edges = cv2.dilate(edges, kernel_3, iterations = 5)
    # edges = cv2.erode(edges, kernel_2, iterations = 1)
    # edges = cv2.dilate(edges, kernel_2, iterations = 5)
    # edges = cv2.erode(edges, kernel_2, iterations = 1)
    return edges
flag = False
while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.resize(frame, (720, 480))
    if not ret:
        print('Het video')
        break
    
    h = frame.shape[0]
    w = frame.shape[1]
    if flag == False:
        bg = cv2.resize(bg, (w, h))
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

 
    img = cv2.GaussianBlur(img, (3,3), 0)
    thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 13, 5)
    
    # ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    canny = auto_canny(thresh)

    edges = preprocessing(canny)
    
    cnt = sorted(cv2.findContours(edges, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)[-2], key=cv2.contourArea)[-1]
    mask = np.zeros((h, w), np.uint8)
    masked = cv2.drawContours(mask, [cnt], -1, 255, -1)
    kernel = np.ones((5,5), np.uint8)
    masked = cv2.erode(masked, kernel, iterations = 7)
    dst_fg = cv2.bitwise_and(frame, frame, mask=masked)
    mask_inversed = cv2.bitwise_not(masked)
    dst_bg = cv2.bitwise_and(bg, bg, mask=mask_inversed)
    dst = cv2.bitwise_or(dst_fg, dst_bg)
    cv2.imshow('frame', dst_fg)
    if cv2.waitKey(25) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
