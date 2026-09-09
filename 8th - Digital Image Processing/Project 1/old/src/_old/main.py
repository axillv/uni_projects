import cv2
import numpy as np

# load image
image = cv2.imread("img/lenna.jpg", cv2.IMREAD_GRAYSCALE)

tmp = np.float32(image) / 255.0
tmp = cv2.dct(tmp)
# tmp = np.uint8(tmp*255.0)

# tmp = np.float32(tmp) / 255.0
# tmp = cv2.idct(tmp)
# tmp = np.uint8(tmp*255.0)

# show original image
cv2.imshow("Original", image)
cv2.imshow("Compressed", tmp)
cv2.waitKey(0)





# # load image
# image = cv2.imread("img/lenna.jpg", cv2.IMREAD_GRAYSCALE)
# image = cv2.resize(image, (32, 32))
# image = np.float32(image) / 255.0
# dct = cv2.dct(image)
# imgcv1 = np.uint8(dct*255.0)

# #show original image
# cv2.imshow("DCT", imgcv1)
# cv2.waitKey(0)