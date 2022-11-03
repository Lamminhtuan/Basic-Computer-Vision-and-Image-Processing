import numpy as np
import matplotlib.pyplot as plt
import random
n = int(input('Enter n: '))
a_ = float(input('Enter a: '))
b_ = float(input('Enter b: '))
while a_ == 0 and b_ == 0:
    a_ = float(input('Enter a: '))
    b_ = float(input('Enter b: '))
c_ = float(input('Enter c: '))
if (b_ < 0):
    print('Line\'s Equation entered: {0}x{1}y={2}'.format(a_, b_, c_))
else:
    print('Line\'s Equation entered: {0}x+{1}y={2}'.format(a_, b_, c_))
n_line = int(0.7 * n)
n_non = n - n_line
if b_ != 0:
    x = np.linspace(0, n, n_line, dtype=int)
    y = (a_ * x + c_) / -b_
else:
    x = np.ones(n) * (-c_/a_)
    y = np.arange(n)
#Add noise
x_noise = np.random.randint(n, size=n_non)
y_noise = np.random.randint(n, size=n_non)
x_zip = np.append(x, x_noise)
y_zip = np.append(y, y_noise)
cor = list(zip(x_zip, y_zip))
cor_ = cor.copy()
def plot_line(a, b, c):
    if b != 0:
        x_ = np.arange(n * 2)
        y_ = (a * x_ + c) / -b
    else:
        x_ = np.ones(n * 2) * (-c/a)
        y_ = np.arange(n * 2)
    plt.scatter(x, y, color = 'g')
    plt.scatter(x_noise, y_noise, color = 'r')
    plt.plot(x_, y_)
    plt.title('Line\'s Equation Finding')
    plt.show(block=False)
    plt.pause(2)
    plt.close()
#GCD 
def gcd(x, y):
    while(y):
        x, y = y, x % y
    return x
#Line's equation
def line_equation(cor1, cor2):
    x1, y1 = cor1
    x2, y2 = cor2
    a = y2 - y1
    b = x1 - x2
    c = -(a*x1 + b*y1)
    gcd_1 = gcd(a, b)
    gcd_all = gcd(gcd_1, c)
    #Simplifying 
    a = float(a / gcd_all)
    b = float(b / gcd_all)
    c = float(c / gcd_all)
    return a, b, c
#Check whether a point on line
def checkonline(cor, a, b, c):
    x, y = cor
    k = a * x + b * y + c
    return k == 0

flag = True
while flag == True:
    count = 2
    cor = cor_.copy()
    random.shuffle(cor)
    cor1 = cor.pop()
    cor2 = cor.pop()
    a, b, c = line_equation(cor1, cor2)
    plot_line(a, b, c)
    for i in cor:
        if checkonline(i, a, b, c) == True:
            count += 1
        if count >= n_line:
            if (b < 0):
                print('Line\'s Equation found: {0}x{1}y={2}'.format(a, b, c))
            else:
                print('Line\'s Equation found: {0}x+{1}y={2}'.format(a, b, c))
            flag = False
            break
         

