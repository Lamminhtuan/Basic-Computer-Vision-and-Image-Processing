import matplotlib.pyplot as plt
import cv2
from imutils.object_detection import non_max_suppression
import numpy as np
# Normalized cross - correlation
def norm_correlation(input, template):
    a_ = input.flatten()
    b_ = template.flatten()
    c = np.sum(a_**2)
    d = np.sum(b_**2)
    return np.dot(a_, b_) / np.sqrt(c * d)

input = cv2.imread('./images/9-ro.jpeg')
template = cv2.imread('./images/template.png')
inp_gray = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
tem_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

inp_gray = inp_gray.astype('float64')
tem_gray = tem_gray.astype('float64')
h_a, w_a = inp_gray.shape
h_b, w_b = tem_gray.shape

thresh_hold = 0.95
thresh_hold_big = 0.97
# Tìm template nhỏ
height = (h_a - h_b) + 1
width = (w_a - w_b) + 1
result = np.ones((height, width), dtype=np.float64)
for i in range(result.shape[0]):
    for j in range(result.shape[1]):
        result[i][j] = norm_correlation(inp_gray[i:i+h_b, j:j+w_b], tem_gray)
(yb_points, xb_points) = np.where(result >= thresh_hold)
boxes = []
for (xb, yb) in zip(xb_points, yb_points):
    boxes.append((xb, yb, xb + w_b, yb + h_b))
boxes_nms = non_max_suppression(np.array(boxes))
print(len(boxes_nms))
for (x1b, y1b, x2b, y2b) in boxes_nms:
    cv2.rectangle(input, (x1b, y1b), (x2b, y2b), (255, 0, 0), 1)

# Show kết quả trực quan hóa và vị trí cực đại hóa

cv2.imshow('Detected point', input)
cv2.waitKey(0)
