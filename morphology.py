import cv2
import numpy as np
ori = cv2.imread('./images/tebaomau.png')
img = cv2.cvtColor(ori, cv2.COLOR_BGR2GRAY)
#Nhị phân hóa ảnh
ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
img = cv2.bitwise_not(img)
kernel = np.ones((30, 30), np.uint8)
kernel_ero_1 = np.ones((10, 10), np.uint8)
kernel_ero_2 = np.ones((4, 4), np.uint8)
kernel_ero_3 = np.ones((2, 2), np.uint8)
opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
erosion = cv2.erode(opening,kernel_ero_1,iterations = 1)
erosion = cv2.erode(erosion,kernel_ero_2,iterations = 1)
erosion = cv2.erode(erosion,kernel_ero_3,iterations = 1)
contour_img = ori.copy()
contours = cv2.findContours(erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]
index = 1
isolated_count = 0
cluster_count = 0
for cntr in contours:
    area = cv2.contourArea(cntr)
    convex_hull = cv2.convexHull(cntr)
    convex_hull_area = cv2.contourArea(convex_hull)
    ratio = area / convex_hull_area
    if ratio < 0.91:
        #Liên thông màu đỏ
        cv2.drawContours(contour_img, [cntr], 0, (0,0,255), 2)
        cluster_count = cluster_count + 1
    else:
        #Độc lập màu xanh
        cv2.drawContours(contour_img, [cntr], 0, (0,255,0), 2)
        isolated_count = isolated_count + 1
    index = index + 1
    
print('number_clusters:',cluster_count)
print('number_isolated:',isolated_count)
print('Number of blood cells', cluster_count + isolated_count)
cv2.imshow("erosion", erosion)
cv2.imshow("result", contour_img)
cv2.waitKey(0)

