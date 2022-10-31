import numpy as np
import matplotlib.pyplot as plt
import random

x = np.arange(7)
y = 5 * x + 3
x_noise = np.random.randint(10, size=3)
y_noise = np.random.randint(40, size=3)
x = np.append(x, x_noise)
y = np.append(y, y_noise)
cor = list(zip(x, y))
n = len(cor)
n_oline = int(0.7 * n)
cor_ = cor.copy()
def plot_line(a, b, c, x_range, y_range):
    if b != 0:
        x_ = np.arange(x_range)
        y_ = (a * x_ + c) / -b
    else:
        x_ = np.ones(y_range) * (-c/a)
        y_ = np.arange(y_range)

    plt.scatter(x, y)
    plt.plot(x_, y_)
    plt.show(block=False)
    plt.pause(1)
    plt.close()


def gcd(x, y):
    while(y):
        x, y = y, x % y
    return x


def line_equation(cor1, cor2):
    x1, y1 = cor1
    x2, y2 = cor2
    a = y2 - y1

    b = x1 - x2
    c = -(a*x1 + b*y1)
    gcd_1 = gcd(a, b)
    gcd_all = gcd(gcd_1, c)
    a = int(a / gcd_all)
    b = int(b / gcd_all)
    c = int(c / gcd_all)
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
    plot_line(a, b, c, 11, 41)
    for i in cor:
        if checkalongline(i, a, b, c) == True:
            count += 1

    if count == n_oline:
        if (b < 0):
            print('{0}x{1}y={2}'.format(a, b, c))
        else:
            print('{0}x+{1}y={2}'.format(a, b, c))
        break
