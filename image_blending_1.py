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

bgs = frames
for i in range(len(frames)):
    bgs[i] = cv2.resize(frames[i], dim)
fg = cv2.cvtColor(fg, cv2.COLOR_BGR2RGBA)
fg[mask[:,:,3] == 0] = 0
alpha = 0.3
results = []
h = height // 2
fg_top = fg[:h,:,:]
fg_bot = fg[h:,:,:]
mask_top = mask[:h,:,:]
mask_bot = mask[h:,:,:]
cv2.imwrite('fg_top.png',fg_top)
for i in range(len(bgs)):
    result = fg.copy()
    bgs_top = bgs[i][:h,:,:]

 
    result[:h,:,:][mask_top[:,:,3] == 0] = fg_top[mask_top[:,:,3] == 0] * alpha \
    + bgs_top[mask_top[:,:,3] == 0] * (1 - alpha)
    
    results.append(result)
for i in range(len(results)):
    dst = cv2.addWeighted(fg_bot, 0.8, bgs[i][h:,:,:], 0.2, 0)
    results[i][h:,:,:] = dst

# for i in range(len(results)):
#     topleft = (400, 201)
#     bottomright = (611, 203)
#     x, y = topleft[0], topleft[1]
#     w, h = bottomright[0]-topleft[0], bottomright[1]-topleft[1]
#     ROI = results[i][y:y+h, x:x+w]
#     blur = cv2.GaussianBlur(ROI, (51,51), 0) 
#     results[i][y:y+h, x:x+w] = blur
imageio.mimsave('result_1.gif', results)