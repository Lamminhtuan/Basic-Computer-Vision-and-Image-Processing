import matplotlib.pyplot as plt
import cv2
from imutils.object_detection import non_max_suppression
import numpy as np
# Chuẩn hóa ảnh
def normalize_image(input):
    input[:, :, 0] = 255 * ((input[:, :, 0] - input[:, :, 0].min()) /
                            (input[:, :, 0].max() - input[:, :, 0].min()))
    input[:, :, 1] = 255 * ((input[:, :, 1] - input[:, :, 1].min()) /
                            (input[:, :, 1].max() - input[:, :, 1].min()))
    input[:, :, 2] = 255 * ((input[:, :, 2] - input[:, :, 2].min()) /
                            (input[:, :, 2].max() - input[:, :, 2].min()))
    return input
# Normalized cross - correlation
def norm_correlation(input, template):
    a_ = input.flatten()
    b_ = template.flatten()
    c = np.sum(a_**2)
    d = np.sum(b_**2)
    return np.dot(a_, b_) / np.sqrt(c * d)

input = cv2.imread('./images/9-ro-dark.jpeg')
template = cv2.imread('./images/template.png')
inp = normalize_image(input)
tem = normalize_image(template)
inp_gray = cv2.cvtColor(inp, cv2.COLOR_BGR2GRAY)
tem_gray = cv2.cvtColor(tem, cv2.COLOR_BGR2GRAY)
tem_big_gray = cv2.resize(tem_gray, (146, 148))

inp_gray = inp_gray.astype('float64')
tem_gray = tem_gray.astype('float64')
tem_big_gray = tem_big_gray.astype('float64')
h_a, w_a = inp_gray.shape
h_b, w_b = tem_gray.shape
h_c, w_c = tem_big_gray.shape

thresh_hold = 0.945
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
for (x1b, y1b, x2b, y2b) in boxes_nms:
    cv2.rectangle(inp, (x1b, y1b), (x2b, y2b), (255, 0, 0), 1)
# Tìm template to
height_big = (h_a - h_c) + 1
width_big = (w_a - w_c) + 1
result_big = np.ones((height_big, width_big), dtype=np.float64)
for i in range(result_big.shape[0]):
    for j in range(result_big.shape[1]):
        result_big[i][j] = norm_correlation(
            inp_gray[i:i+h_c, j:j+w_c], tem_big_gray)
(yc_points, xc_points) = np.where(result_big >= thresh_hold_big)
boxes_big = []
for (xc, yc) in zip(xc_points, yc_points):
    boxes_big.append((xc, yc, xc + w_c, yc + h_c))
boxes_big_nms = non_max_suppression(np.array(boxes_big))
for (x1c, y1c, x2c, y2c) in boxes_big_nms:
    cv2.rectangle(inp, (x1c, y1c), (x2c, y2c), (255, 0, 0), 1)
print('Đây là lá', len(boxes_big_nms), 'rô')
# Show kết quả trực quan hóa và vị trí cực đại hóa
plt.subplot(121)
plt.imshow(result, cmap='gray')
plt.title('Ket qua ccorr_normed template nho')
plt.subplot(122)
plt.imshow(result_big, cmap='gray')
plt.title('Ket qua ccorr_normed voi template to')
plt.show()
cv2.imshow('Detected point', input)
cv2.waitKey(0)
