import cv2
import numpy as np
import matplotlib.pyplot as plt
import random
a = cv2.imread('images/sea.jpg')
x = np.arange(7)
y = 5 * x + 3
x_noise = np.random.randint(10, size=3)
y_noise = np.random.randint(40, size=3)
x = np.append(x, x_noise)
y = np.append(y, y_noise)
cor = list(zip(x, y))
cor_ = cor.copy()
def line_equation(cor1, cor2):
    x1, y1 = cor1
    x2, y2 = cor2
    a = y2 - y1
    b = x1 - x2
    c = -(a*x1 + b*y1)
    return a, b, c
def checkalongline(cor, a, b, c):
    x, y = cor
    k = a * x + b * y + c
    return k == 0
while True:
    count = 2
    cor = cor_.copy()
    random.shuffle(cor)
    cor1 = cor.pop()
    cor2 = cor.pop()
    a, b, c = line_equation(cor1, cor2)
    for i in cor:
        if checkalongline(i, a, b, c) == True:
            count += 1
    if count == 7:
        fig = plt.figure()
        x1, y1= cor1
        x2, y2 = cor2
        plt.scatter(x1, y1)
        plt.scatter(x2, y2)
        plt.plot((x1, x2), (y1, y2))
        plt.show()
        if (b < 0):
            print(a, 'x ', b, ' = ', c)
        else:
            print(a, 'x + ', b, ' = ', c)

        break
