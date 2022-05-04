import cv2
import numpy as np
import matplotlib.pyplot as plt

file = "color.jpg"

img = cv2.imread(file)
img = cv2.resize(img, (640,680))

plt.imshow(img)
plt.show()

imhsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
imhsv = cv2.boxFilter(imhsv, -1, (10,10))

h_img = imhsv[:, :, 0]
s_img = imhsv[:, :, 1]
v_img = imhsv[:, :, 2]

hfilt = cv2.boxFilter(imhsv[:, :, 0], cv2.CV_32F, (40, 40))
sfilt = cv2.boxFilter(imhsv[:, :, 1], cv2.CV_32F, (40, 40))
vfilt = cv2.boxFilter(imhsv[:, :, 2], cv2.CV_32F, (40, 40))

fig, ax = plt.subplots(1,3, figsize = (15, 10))

ax[0].imshow(hfilt, cmap="summer")
ax[1].imshow(sfilt, cmap="Greens")
ax[2].imshow(vfilt, cmap="Greens")


plt.show()


img_thresh_hue = np.logical_and(imhsv[:,:,0] > -10, imhsv[:,:,0] < 180)
img_thresh_sat = np.logical_and(imhsv[:,:,1] > 35, imhsv[:,:,1] < 300)
img_thresh_HS = np.logical_and(img_thresh_hue,img_thresh_sat)
img_thresh_val = np.logical_and(imhsv[:,:,2] > 100, imhsv[:,:,2] < 300)
img_thresh_HSV = np.logical_and(img_thresh_HS, img_thresh_val)

imdec = cv2.boxFilter(img_thresh_HSV.astype(int), -1, (10,10), normalize=False)

imdec_threshold = np.argwhere(imdec>1000)

fig, ax = plt.subplots(1,3)
ax[0].imshow(img_thresh_hue, cmap = "gray")
ax[1].imshow(img_thresh_sat, cmap = "gray")
ax[2].imshow(img_thresh_val, cmap = "gray")

plt.show()

plt.imshow(img_thresh_HS, cmap = "gray")
plt.title("HS")

plt.show()

plt.imshow(img_thresh_HSV, cmap = "gray")
plt.title("HSV")

plt.show()

plt.imshow(imdec, cmap = "gray")
plt.title("imdec")

plt.show()


pixel_pos = np.average(imdec_threshold, axis = 0)
print(pixel_pos)

plt.imshow(img)
plt.imshow(imdec)

plt.plot(pixel_pos[0], pixel_pos[1], "bo")
plt.show()

 


