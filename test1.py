import numpy as np
import cv2 
a  = np.array([[7, 8, 27, 20],
                [3, 4, 3, 25],
                [5, 6, 22, 21]], dtype=np.int16)
def calculate_gradient(a):
    b_n = (np.pad(a[1:, :], ((0, 1), (0, 0)), 'constant') - a) ** 2
    c_n = (np.pad(a[:, 1:], ((0, 0), (0,1)), 'constant') - a) ** 2
    result = np.sqrt(b_n + c_n)
    return result
print(calculate_gradient(a))