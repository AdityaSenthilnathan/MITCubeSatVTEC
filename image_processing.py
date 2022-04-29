import cv2
import numpy as np
import matplotlib.pyplot as plt

file = ""
image = cv2.imread(file)

rfilt = image[:, :, 2]
gfilt = image[:, :, 1]
bfilt = image[:, :, 0]

rfilt = cv2.boxFilter(image[:,:,2], cv2.CV_32F, (100,100))
gfilt = cv2.boxFilter(image[:,:,1], cv2.CV_32F, (100,100))
bfilt = cv2.boxFilter(image[:,:,0], cv2.CV_32F, (100,210))

fig, ax = plt.subplots(1,3, figsize = (15, 10))
ax[2].imshow(rfilt, cmap="Reds")
ax[1].imshow(gfilt, cmap="Greens")
ax[0].imshow(bfilt, cmap="Blues")
plt.show()

mask = cv2.inRange(rfilt, 16.9, 17)
plt.imshow(mask)
plt.colorbar()
plt.imshow
plt.title("Mask")
plt.show()

sat = cv2.inRange(gfilt, 135, 190)
plt.imshow(sat)
plt.colorbar()
plt.title("Saturation")
plt.show()


val = cv2.inRange(bfilt, 40, 80)
plt.imshow(val)
plt.colorbar()
plt.title("Value")
plt.show()

res = cv2.bitwise_and(image, image, mask=mask)
plt.imshow(res)
plt.show()
