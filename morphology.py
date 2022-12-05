import cv2
import numpy as np
s = cv2.imread('images/face.jpg')
d = cv2.imread('images/cat.jpg')
d = cv2.resize(d, (s.shape[1], s.shape[0]))
for f in range(0, 3*24):
    t = f / (3 * 24)
    tt = s.copy()
    tt = ((1-t) * s + t * d).astype(np.uint8)
    cv2.imshow('result', tt)
    cv2.waitKey(10)
