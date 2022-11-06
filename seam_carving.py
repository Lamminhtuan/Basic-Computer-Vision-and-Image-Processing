import cv2
import numpy as np
from numba.experimental import jitclass
a = cv2.imread('images/relationship.jpg')
def calculate_derative(a):
    b_n = (np.pad(a[1:, :], ((0, 1), (0, 0)), 'constant') - a) ** 2
    c_n = (np.pad(a[:, 1:], ((0, 0), (0, 1)), 'constant') - a) ** 2
    return np.sqrt(b_n + c_n)
def calculate_gradient(img):
    b,g, r = cv2.split(img)
    b = calculate_derative(b)
    g = calculate_derative(g)
    r = calculate_derative(r)
    return b + g + r

def find_min_seam(img):
    h, w, _ = img.shape
    e = calculate_gradient(img)
    
    dyn = e.copy()
    find_path = np.zeros(e.shape, dtype=np.int32)
    for i in range(1, h):
        for j in range(w):
            if j == 0:
                idx = np.argmin(dyn[i-1,j:j+2])
                find_path[i, j] = idx + j
                min_e = dyn[i-1,idx + j]
            else:
                idx = np.argmin(dyn[i-1, j-1:j+2])        
                find_path[i, j] = idx +j  -1
                min_e = dyn[i-1,idx + j- 1]
            dyn[i, j]+=min_e
    return dyn, find_path

def crop_column(img):
    h, w, _ = img.shape
    dyn, find_path = find_min_seam(img)
    mask = np.ones((h, w), dtype=bool)
    j = np.argmin(dyn[-1])
    for i in reversed(range(h)):
        mask[i, j] = False
        j = find_path[i, j]
    mask = np.dstack([mask] * 3)
    
    img = img[mask].reshape((h,w-1, 3))
    return img
def crop_multi_columns(img, scale):
    h, w, _ = img.shape
    new_w = int(scale * w)
    for i in range(w - new_w):
        img = crop_column(img)
    return img
scale = float(input('Enter scale for cropping: '))
result = crop_multi_columns(a, scale)
cv2.imshow('original', a)
cv2.imshow('cropped', result)
cv2.waitKey(0)


