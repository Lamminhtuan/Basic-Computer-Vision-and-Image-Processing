import cv2
import numpy as np
inp = cv2.imread('./images/9-ro.jpeg')
tem = cv2.imread('./images/template.png')
a = cv2.cvtColor(inp, cv2.COLOR_BGR2GRAY)
b = cv2.cvtColor(tem, cv2.COLOR_BGR2GRAY)
a = a.astype('float64')
b = b.astype('float64')
h_a, w_a = a.shape
h_b, w_b = b.shape


def norm_correlation(input, template):
    
    a_ = input.flatten()
    b_ = template.flatten()
    c = np.sum(a_**2)
    d = np.sum(b_**2)

    return np.dot(a_, b_) / np.sqrt(c * d)


height = (h_a - h_b) + 1
width = (w_a - w_b) + 1
result = np.ones((height, width), dtype=np.float64)
thresh_hold = 0.95
for i in range(result.shape[0]):
    for j in range(result.shape[1]):
        result[i][j] = norm_correlation(a[i:i+h_b, j:j+w_b], b)
(y_points, x_points) = np.where(result >= thresh_hold)
boxes = []
for (x, y) in zip(x_points, y_points):
    boxes.append((x, y, x + w_b, y + h_b))
for (x1, y1, x2, y2) in boxes:
    cv2.rectangle(inp, (x1, y1), (x2, y2),
                  (255, 0, 0), 1)
cv2.imshow("Template matching", inp)
cv2.waitKey(0)
