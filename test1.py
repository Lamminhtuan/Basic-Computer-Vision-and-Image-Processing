import numpy as np
import matplotlib.pyplot as plt
x = np.arange(7)
y = -3 * x + 3
fig = plt.figure()
plt.plot(x, y)
plt.show(block=False)
plt.close()