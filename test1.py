import cv2 
a = cv2.imread('images/relationship.jpg')
b, g, r = cv2.split(a)
result = b + g + r
print(result.shape)