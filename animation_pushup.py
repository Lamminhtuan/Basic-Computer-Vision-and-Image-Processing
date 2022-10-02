import cv2
import numpy as np

#Buoc 1: Doc anh tu file
img1 = cv2.imread('1.jpg')
img2 = cv2.imread('2.jpg')
#Buoc 2: Vong lap voi D
view = img1.copy()
H =img1.shape[0]


for D in range(H,0,-1):
    
    view[D:,:]= img1[D:,:]
    #Buoc 2.1 Cat phan dau cua view hien thi
    view[0:D,:] = img2[H-D:,:]
    #Buoc 2.2. Cat phan cuoi cua view hien thi
    
    #Buoc 2.3. Hien thi anh
    cv2.imshow('View', view)
    cv2.waitKey(15)
#pixel wised tranform
#double exposure
