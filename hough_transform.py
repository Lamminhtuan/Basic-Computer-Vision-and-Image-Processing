import cv2
import numpy as np

img = cv2.imread('images/football.png')
def calculate_derative(a):
    b_n = (np.pad(a[1:, :], ((0, 1), (0, 0)), 'constant') - a) ** 2
    c_n = (np.pad(a[:, 1:], ((0, 0), (0, 1)), 'constant') - a) ** 2
    return np.sqrt(b_n + c_n)

#calculate gradient for each channel and combine them
def calculate_gradient(img):
    b, g, r = cv2.split(img)
    b = calculate_derative(b)
    g = calculate_derative(g)
    r = calculate_derative(r)
    return b + g + r
def line_detect(img):
    #y for rows and x for columns
    
    h = img.shape[0]
    w = img.shape[1]
    #step 1: calculate the energy
    energy = calculate_gradient(img).astype(np.uint8)
    # energy = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # energy = cv2.Canny(energy, 50, 150, apertureSize=3)
    #calculate the max rho possible
    max_dist = int(np.round(np.sqrt(h**2 + w**2)))
    theta_range = np.arange(-3.14, 3.14, 0.01)
    #rows denote the rho and columns denote the theta
    #step 2:init the Hough table
    H = np.zeros((max_dist, len(theta_range)), dtype=np.uint8)
    #step 3: for each pixel in energy, calculate the rho
    for y in range(h):
        for x in range(w):
        
            if energy[y][x] > 0:
                for theta in theta_range:
                    
                    rho = x * np.cos(theta) + y * np.sin(theta)
                    #if rho in Hough space
                    if rho >= 0 and rho < max_dist:
                        #map from Hough space to matrix
                        H[int(rho), int((theta + 3.14)/0.01)] += 1
    threshold = 250
    #voting...
    list_ = np.where(H >= threshold)
    rho = list_[0]
    #map from matrix to Hough space
    theta = list_[1] * 0.01 - 3.14
    for i in range(len(rho)):
        #polar to cartesian
        a = np.cos(theta[i])
        b = np.sin(theta[i])
        #x0 = rho * cos(theta)
        x0 = a * rho[i]
        #y0 = rho * sin(theta)
        y0 = b * rho[i]
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000 * a)
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*a)
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 1)
    return img
result = line_detect(img)
cv2.imwrite('lines_detected.png', result)
cv2.waitKey(0)