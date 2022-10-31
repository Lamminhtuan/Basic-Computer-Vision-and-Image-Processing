import cv2
import numpy as np
a = cv2.imread('images/pen.jpg')
a = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
def calculate_gradient(a):
    b_n = (np.pad(a[1:, :], ((0, 1), (0, 0)), 'constant') - a) ** 2
    c_n = (np.pad(a[:, 1:], ((0, 0), (0,1)), 'constant') - a) ** 2
    result = np.sqrt(b_n + c_n)
    return result
cv2.imshow('ori', a)
print(a.max())
print(calculate_gradient(a).max())
b = calculate_gradient(a).astype(np.uint8)
cv2.imshow('grad', b)
cv2.waitKey(0)

