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
    frames[i] = cv2.resize(frames[i], dim)
fg = cv2.cvtColor(fg, cv2.COLOR_BGR2RGBA)
alpha = 0.8
results = []
h = height // 2
fg_top = fg[:h,:,:]
fg_bot = fg[h:,:,:]
mask_top = mask[:h,:,:]
mask_bot = mask[h:,:,:]
cv2.imwrite('fg_top.png',fg_top)
for i in range(len(frames)):
    result = fg.copy()
    result[:h,:,:][mask_top[:,:,3] == 0] = frames[i][:h,:,:][mask_top[:,:,3]==0]
    results.append(result)
for i in range(len(results)):
    results[i][h:,:,:][mask_bot[:,:,3] != 0] = fg_bot[mask_bot[:,:,3] != 0] * alpha \
    + frames[i][h:,:,:][mask_bot[:,:,3] != 0] * (1 - alpha)
    results[i][h:,:,:][mask_bot[:,:,3] == 0] = frames[i][h:,:,:][mask_bot[:,:,3]==0]
imageio.mimsave('result_complex.gif', results)