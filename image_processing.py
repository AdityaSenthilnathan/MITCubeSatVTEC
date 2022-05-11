import cv2
import numpy as np
import matplotlib.pyplot as plt

def pShow(img, colorspace="HSV"):
    if colorspace == "HSV":
        cimg = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
    elif colorspace == "BGR":
        cimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        cimg = img

    plt.imshow(cimg)
    plt.show()

file = "color.jpg"
img = cv2.imread(file)
#img = cv2.resize(img, (640,680))
 
plt.imshow(np.flip(img, axis=2))
plt.show()

imhsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
plt.imshow(imhsv, cmap="hsv")
plt.show()


fil_imhsv = cv2.boxFilter(imhsv, -1, (40, 40))
plt.imshow(fil_imhsv, cmap="hsv")
plt.show()

plt.imshow(fil_imhsv[:, :, 0])
plt.show()

plt.imshow(fil_imhsv[:, :, 1])
plt.show()

plt.imshow(fil_imhsv[:, :, 2])
plt.show()

thresh_hue = np.logical_and( 29 < fil_imhsv[:, :, 1], fil_imhsv[:, :, 1] < 360)
plt.imshow(thresh_hue, cmap="gray")
plt.show()

thresh_sat = np.logical_and(0 < fil_imhsv[:, :, 0], fil_imhsv[:, :, 0] < 360)
plt.imshow(thresh_sat, cmap="gray")
plt.show()

thresh_HS = np.logical_and(thresh_hue, thresh_sat)
plt.imshow(thresh_HS, cmap="gray")
plt.show()

thresh_val =  np.logical_and(100 <= fil_imhsv[:, :, 2], fil_imhsv[:, :, 2] < 300)
plt.imshow(thresh_val, cmap="gray")
plt.show()

img_thresh = np.logical_and(thresh_HS, thresh_val)
plt.imshow(img_thresh, cmap="gray")
plt.show()

img_fil_no_norm = cv2.boxFilter(thresh_HS.astype(int), -1, (10,10), normalize=False)
plt.imshow(img_fil_no_norm)
plt.show()

img_thresh_locs = np.argwhere(img_fil_no_norm > 10)
print(img_thresh_locs)

average_loc = np.average(img_thresh_locs, axis=0)

plt.imshow(np.flip(img, axis=2))
plt.plot(img_thresh_locs[:, 1], img_thresh_locs[:, 0], 'ro')

plt.show()

print(np.average(img_thresh_locs, axis=0))

def sensor_position(pix_x, pix_y, res_x, res_y):
    return ((pix_x - res_x / 2) / res_x * 0.00368, (pix_y - res_y / 2) / res_y * 0.00276)

def angle(x, y):
    print((np.arctan(x / 0.00304), np.arctan(y / 0.00304)))
    return np.degrees((np.arctan(x / 0.00304), np.arctan(y / 0.00304)))

position = sensor_position(average_loc[1], average_loc[0], 640, 360)
print(position)
angle(*position)

no_norm_8 = img_fil_no_norm.astype(np.uint8)
thresh, no_norm_out = cv2.threshold(no_norm_8, 1000 * 255 / np.max(img_fil_no_norm), 255, cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(no_norm_out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

print(contours)
[np.average(contour, axis=0) for contour in contours]





# thresh_hue_r = np.logical_and(241 < fil_imhsv[:, :, 1], fil_imhsv[:, :, 1] < 300)
# plt.imshow(thresh_hue_r, cmap="gray")
# plt.show()

# thresh_sat_r = np.logical_and( 100< fil_imhsv[:, :, 0], fil_imhsv[:, :, 0] < 150)
# plt.imshow(thresh_sat_r, cmap="gray")
# plt.show()

# thresh_HS_r = np.logical_and(thresh_hue_r, thresh_sat_r)
# plt.imshow(thresh_HS_r, cmap="gray")
# plt.show()

# thresh_val_r =  np.logical_and(100 <= fil_imhsv[:, :, 2], fil_imhsv[:, :, 2] < 250)
# plt.imshow(thresh_val_r, cmap="gray")
# plt.show()

# img_thresh_r = np.logical_and(thresh_HS_r, thresh_val_r)
# plt.imshow(img_thresh_r, cmap="gray")
# plt.show()

# img_fil_no_norm_r = cv2.boxFilter(thresh_HS_r.astype(int), -1, (10,10), normalize=False)
# plt.imshow(img_fil_no_norm_r)
# plt.show()

# img_thresh_locs_r = np.argwhere(img_fil_no_norm_r > 10)
# print(img_thresh_locs_r)

# average_loc_r = np.average(img_thresh_locs_r, axis=0)

# plt.imshow(np.flip(img, axis=2))
# plt.plot(img_thresh_locs_r[:, 1], img_thresh_locs_r[:, 0], 'ro')

# plt.show()

# print(np.average(img_thresh_locs_r, axis=0))

# def sensor_position(pix_x, pix_y, res_x, res_y):
#     return ((pix_x - res_x / 2) / res_x * 0.00368, (pix_y - res_y / 2) / res_y * 0.00276)

# def angle(x, y):
#     print((np.arctan(x / 0.00304), np.arctan(y / 0.00304)))
#     return np.degrees((np.arctan(x / 0.00304), np.arctan(y / 0.00304)))

# position = sensor_position(average_loc_r[1], average_loc_r[0], 640, 360)
# print(position)
# angle(*position)

# no_norm_8 = img_fil_no_norm_r.astype(np.uint8)
# thresh, no_norm_out = cv2.threshold(no_norm_8, 1000 * 255 / np.max(img_fil_no_norm_r), 255, cv2.THRESH_BINARY)

# contours, hierarchy = cv2.findContours(no_norm_out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# print(contours)
# [np.average(contour, axis=0) for contour in contours]

# thresh_hue_r = np.logical_and(36 < fil_imhsv[:, :, 1], fil_imhsv[:, :, 1] < 70)
# plt.imshow(thresh_hue_r, cmap="gray")
# plt.show()

# thresh_sat_r = np.logical_and(100< fil_imhsv[:, :, 0], fil_imhsv[:, :, 0] < 155)
# plt.imshow(thresh_sat_r, cmap="gray")
# plt.show()

# thresh_HS_r = np.logical_and(thresh_hue_r, thresh_sat_r)
# plt.imshow(thresh_HS_r, cmap="gray")
# plt.show()

# thresh_val_r =  np.logical_and(100 <= fil_imhsv[:, :, 2], fil_imhsv[:, :, 2] < 155)
# plt.imshow(thresh_val_r, cmap="gray")
# plt.show()

# img_thresh_r = np.logical_and(thresh_HS_r, thresh_val_r)
# plt.imshow(img_thresh_r, cmap="gray")
# plt.show()

# img_fil_no_norm_r = cv2.boxFilter(thresh_HS_r.astype(int), -1, (10,10), normalize=False)
# plt.imshow(img_fil_no_norm_r)
# plt.show()

# img_thresh_locs_r = np.argwhere(img_fil_no_norm_r > 10)
# print(img_thresh_locs_r)

# average_loc_r = np.average(img_thresh_locs_r, axis=0)

# plt.imshow(np.flip(img, axis=2))
# plt.plot(img_thresh_locs_r[:, 1], img_thresh_locs_r[:, 0], 'ro')

# plt.show()

# print(np.average(img_thresh_locs_r, axis=0))

# def sensor_position(pix_x, pix_y, res_x, res_y):
#     return ((pix_x - res_x / 2) / res_x * 0.00368, (pix_y - res_y / 2) / res_y * 0.00276)

# def angle(x, y):
#     print((np.arctan(x / 0.00304), np.arctan(y / 0.00304)))
#     return np.degrees((np.arctan(x / 0.00304), np.arctan(y / 0.00304)))

# position = sensor_position(average_loc_r[1], average_loc_r[0], 640, 360)
# print(position)
# angle(*position)

# no_norm_8 = img_fil_no_norm_r.astype(np.uint8)
# thresh, no_norm_out = cv2.threshold(no_norm_8, 1000 * 255 / np.max(img_fil_no_norm_r), 255, cv2.THRESH_BINARY)

# contours, hierarchy = cv2.findContours(no_norm_out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# print(contours)
# [np.average(contour, axis=0) for contour in contours]




# imhsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# imhsv = cv2.boxFilter(imhsv, -1, (10,10))

# h_img = imhsv[:, :, 0]
# s_img = imhsv[:, :, 1]
# v_img = imhsv[:, :, 2]

# hfilt = cv2.boxFilter(imhsv[:, :, 0], cv2.CV_32F, (40, 40))
# sfilt = cv2.boxFilter(imhsv[:, :, 1], cv2.CV_32F, (40, 40))
# vfilt = cv2.boxFilter(imhsv[:, :, 2], cv2.CV_32F, (40, 40))

# fig, ax = plt.subplots(1,3, figsize = (15, 10))

# ax[0].imshow(hfilt, cmap="summer")
# ax[1].imshow(sfilt, cmap="Greens")
# ax[2].imshow(vfilt, cmap="Greens")


# plt.show()


# img_thresh_hue = np.logical_and(imhsv[:,:,0] > 0, imhsv[:,:,0] < 360)
# img_thresh_sat = np.logical_and(imhsv[:,:,1] > 29, imhsv[:,:,1] < 300)

# img_thresh_HS = np.logical_and(img_thresh_hue,img_thresh_sat)
# img_thresh_val = np.logical_and(imhsv[:,:,2] > 100, imhsv[:,:,2] < 300)
# img_thresh_HSV = np.logical_and(img_thresh_HS, img_thresh_val)

# imdec = cv2.boxFilter(img_thresh_HSV.astype(int), -1, (10,10), normalize=False)

# imdec_threshold = np.argwhere(imdec>1000)

# fig, ax = plt.subplots(1,3)
# ax[0].imshow(img_thresh_hue, cmap = "gray")
# ax[1].imshow(img_thresh_sat, cmap = "gray")
# ax[2].imshow(img_thresh_val, cmap = "gray")

# plt.show()

# plt.imshow(img_thresh_HS, cmap = "gray")
# plt.title("HS")

# plt.show()

# plt.imshow(img_thresh_HSV, cmap = "gray")
# plt.title("HSV")

# plt.show()

# plt.imshow(imdec, cmap = "gray")
# plt.title("imdec")

# plt.show()


# pixel_pos = np.average(imdec_threshold, axis = 0)
# print(pixel_pos)

# plt.imshow(img)
# plt.imshow(imdec)

# plt.plot(pixel_pos[0], pixel_pos[1], "bo")
# plt.show()

#try seperating each color and then combine it
