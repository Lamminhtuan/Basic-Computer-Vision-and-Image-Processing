import cv2 
a = cv2.imread('images/relationship.jpg')
cv2.imshow(a.shape[:-1], a)
cv2.waitKey(0)