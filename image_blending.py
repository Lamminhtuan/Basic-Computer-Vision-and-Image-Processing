import cv2
import imageio
import numpy as np
fg_ = cv2.imread('images/tiger.jpg')
mask = cv2.imread('images/tiger_mask.png', cv2.IMREAD_UNCHANGED)
height = mask.shape[0]
width = mask.shape[1]
dim = (width, height)
fg = cv2.resize(fg_, dim)
url = "https://media.giphy.com/media/5xaOcLGm3mKRQuDYCgU/giphy.gif"
frames = imageio.mimread(imageio.core.urlopen(url).read(), '.gif')
for i in range(len(frames)):
    frames[i] = frames[i][:,:,0:3]
    frames[i] = cv2.resize(frames[i], dim)
fg = cv2.cvtColor(fg, cv2.COLOR_BGR2RGB)
alpha = 0.5
results = []
for i in range(len(frames)):
    result = fg.copy()
    result[mask[:,:,3] != 0] = fg[mask[:,:,3] != 0] * alpha \
    + frames[i][mask[:,:,3] != 0] * (1 - alpha)
    results.append(result)
imageio.mimsave('result.gif', results)