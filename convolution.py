import cv2
import numpy as np
#độ dài cạnh kernel
k = 3
a = cv2.imread('images/tiger.jpg')
#Gaussian filter
kernel = np.array([[1, 2, 1],
                   [3, 4, 2],
                   [5, 2, 1]])
# kernel = 1/16 * kernel

kernel = kernel.flatten()
kernel = kernel[::-1]
print(kernel)
a_0 = np.pad(a[:,:,0], (1, ), 'edge')
a_1 = np.pad(a[:,:,1], (1, ), 'edge')
a_2 = np.pad(a[:,:,2], (1, ), 'edge')
result = a.copy()
for i in range(a.shape[0]):
    for j in range(a.shape[1]):
        f_0 = np.dot(a_0[i:i+k,j:j+k].flatten(), kernel)
        f_1 = np.dot(a_1[i:i+k,j:j+k].flatten(), kernel)
        f_2 = np.dot(a_2[i:i+k,j:j+k].flatten(), kernel)
        result[i][j][0] = 255 if f_0 > 255 else f_0
        result[i][j][1] = 255 if f_1 > 255 else f_1
        result[i][j][2] = 255 if f_2 > 255 else f_2
cv2.imshow('Original', a)
cv2.imshow('Result_convolution', result)
cv2.waitKey(0)