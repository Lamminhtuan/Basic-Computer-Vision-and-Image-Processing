import cv2
import numpy as np
from numba import jit
import time
a = cv2.imread('images/cat.jpg')

#calculate gradient on 2d
def calculate_derative(a):
    b_n = (np.pad(a[1:, :], ((0, 1), (0, 0)), 'constant') - a) ** 2
    c_n = (np.pad(a[:, 1:], ((0, 0), (0, 1)), 'constant') - a) ** 2
    return np.sqrt(b_n + c_n)

#calculate gradient for each channel and combine them
def calculate_gradient(img):
    b, g, r = cv2.split(img)
    b = calculate_derative(b)
    g = calculate_derative(g)
    r = calculate_derative(r)
    return b + g + r

#use jit to compile code faster
@jit(forceobj=True)
def find_min_seam(img):
    h, w, _ = img.shape
    e = calculate_gradient(img)
    #matrix for dynamic programming
    dyn = e.copy()
    #store the path for finding minium seam
    find_path = np.zeros(e.shape, dtype=np.int32)
    for i in range(1, h):
        for j in range(w):
            if j == 0:
                idx = np.argmin(dyn[i-1, j:j+2])
                find_path[i, j] = idx + j
                min_e = dyn[i-1, idx + j]
            else:
                idx = np.argmin(dyn[i-1, j-1:j+2])
                find_path[i, j] = idx + j - 1
                min_e = dyn[i-1, idx + j - 1]
            dyn[i, j] += min_e
    return dyn, find_path

#use jit to compile code faster
@jit(forceobj=True)
def crop_column(img):
    h, w, _ = img.shape
    dyn, find_path = find_min_seam(img)
    mask = np.ones((h, w), dtype=bool)
    #minimum value on last row
    j = np.argmin(dyn[-1])
    #finding minimum seam...
    for i in range(h - 1, -1, -1):
        mask[i, j] = False
        j = find_path[i, j]
    mask = np.dstack([mask] * 3)
    img = img[mask].reshape((h, w-1, 3))
    return img


def crop_multi_columns(img, scale):
    h, w, _ = img.shape
    new_w = int(scale * w)
    for i in range(w - new_w):
        img = crop_column(img)
    return img


def crop_multi_rows(img, scale):
    #rotate 90 clockwise and apply crop_multi_columns procedure 
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    img = crop_multi_columns(img, scale)
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return img


d = int(input('Crop horizontally or vertically? (0: Horizontally, 1: Vertically): '))
start = time.time()
while d != 0 and d != 1:
    d = int(input('Crop horizontally or vertically? (0: Horizontally, 1: Vertically): '))
if (d == 0):
    inp = int(input('Enter percents for cropping horizontally (%): '))
    while inp < 0 or inp > 100:
        print('Please enter percents in [0:100]')
        inp = int(input('Enter percents for cropping vertically (%): '))
    scale = inp / 100
    result = crop_multi_columns(a, scale)
elif (d == 1):
    inp = int(input('Enter percents for cropping vertically (%): '))
    while inp < 0 or inp > 100:
        print('Please enter percents in [0:100]')
        inp = int(input('Enter percents for cropping vertically (%): '))
    scale = inp / 100
    result = crop_multi_rows(a, scale)
end = time.time()
print('Time taken', end - start)
print('Original size: ', a.shape[:-1],
      'After cropped size: ', result.shape[:-1])
cv2.imshow('Original', a)
cv2.imshow('Cropped', result)
if d == 0:
    cv2.imwrite('cropped_horizontally.jpg', result) 
elif d == 1:
    cv2.imwrite('cropped_vertically.jpg', result) 
cv2.waitKey(0)
