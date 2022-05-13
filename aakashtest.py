import numpy as np
import matplotlib.pyplot as plt
import cv2

#Reads the image
test = cv2.imread('color.jpg')

plt.imshow(np.flip(test, axis=2))
plt.show()
k = cv2.waitKey(0)
 # Convert BGR to HSV
hsv = cv2.cvtColor(test, cv2.COLOR_BGR2HSV)
plt.imshow(np.flip(hsv, axis=2))
plt.show()
k = cv2.waitKey(0)

  # define range of blue color in HSV
lower_blue = np.array([20,70,50])
upper_blue = np.array([179,255,255])

# Threshold the HSV image to get only blue colors
mask = cv2.inRange(hsv, lower_blue, upper_blue)
cv2.imshow('mask',mask)
k = cv2.waitKey(0)


# define range of blue color in HSV
lower_blue = np.array([100,150,0])
upper_blue = np.array([140,255,255])

# Threshold the HSV image to get only blue colors
mask2 = cv2.inRange(hsv, lower_blue, upper_blue)
cv2.imshow('mask2',mask2)
k = cv2.waitKey(0)


# Bitwise-AND mask and original image
res = cv2.bitwise_or(test,test, mask= mask)
plt.imshow(np.flip(res, axis=2))
plt.show()
k = cv2.waitKey(0)
