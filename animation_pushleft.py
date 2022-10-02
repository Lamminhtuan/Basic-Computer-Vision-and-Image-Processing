import cv2
img1 = cv2.imread('1.jpg')
img2 = cv2.imread('2.jpg')
view = img1.copy()
H = view.shape[1]
for D in range(H,0,-1):
    view[:,:D] = img1[:,H-D:]
    view[:,D:] = img2[:,:H-D]
    cv2.imshow('View', view)
    cv2.waitKey(15)