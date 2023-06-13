import cv2
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
bg = cv2.imread('images/bg.png')
fg = cv2.imread('images/fg.jpg')
img = cv2.imread('images/chromakey.jpg')
trainset = []
testset = []
#Split 3 kênh màu từng hình
b_bg, g_bg, r_bg = cv2.split(bg)
b_fg, g_fg, r_fg = cv2.split(fg)
b_img, g_img, r_img = cv2.split(img)
#Lấy các giá trị màu trong ảnh background và gán class = 0
for i in range(0, b_bg.shape[0]):
    for j in range(0, b_bg.shape[1]):
        row = [b_bg[i, j], g_bg[i, j], r_bg[i, j], 0]
        trainset.append(row)
#Lấy các giá trị màu trong ảnh foreground và gán class = 1
for i in range(0, b_fg.shape[0]):
    for j in range(0, b_fg.shape[1]):
        row = [b_fg[i, j], g_fg[i, j], r_fg[i, j], 1]
        trainset.append(row)
#Tạo tập test từ ảnh cần bỏ background
for i in range(0, b_img.shape[0]):
    for j in range(0, b_img.shape[1]):
        row = [b_img[i, j], g_img[i, j], r_img[i, j]]
        testset.append(row)

trainset = np.asarray(trainset)
testset = np.asarray(testset)
X = trainset[:,:-1]
y = trainset[:, -1]
#Standarize dữ liệu
scaler = StandardScaler()
scaler.fit(X)
X = scaler.transform(X)
testset = scaler.transform(testset)
#Mô hình máy học sử dụng LogisticRegression
model = LogisticRegression()
model.fit(X, y)
y_pred = model.predict(testset)
sum = 0
for i in range(0, b_img.shape[0]):
    for j in range(0, b_img.shape[1]):
        #Nếu dự đoán = 0 thì gán màu đen
        if (y_pred[sum] == 0):
            img[i,j,0] = 0
            img[i,j,1] = 0
            img[i,j,2] =0
        sum += 1
cv2.imshow('background removed', img)
cv2.waitKey(0)