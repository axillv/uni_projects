import cv2
import numpy as np

# load image
image = cv2.imread("img/lenna.jpg", cv2.IMREAD_GRAYSCALE)
# split image into 32x32 blocks
blocks = [image[i:i+32, j:j+32] 
          for i in range(0, image.shape[0], 32) 
          for j in range(0, image.shape[1], 32)]

# apply dct into each block
for i in range(len(blocks)):
    blocks[i] = np.float32(blocks[i]) / 255.0
    blocks[i] = cv2.dct(blocks[i])
    blocks[i] = np.uint8(blocks[i]*255.0)

#TODO: keep different parameters

# apply inverse dct to get original image
for i in range(len(blocks)):
    blocks[i] = np.float32(blocks[i]) / 255.0
    blocks[i] = cv2.idct(blocks[i])
    blocks[i] = np.uint8(blocks[i]*255.0)

# transform blocks back into image
image_comp = np.zeros_like(image)
for i in range(0, len(blocks)):
    image_comp[i//8*32:i//8*32+32, i%8*32:i%8*32+32] = blocks[i]

# show original image
cv2.imshow("Original", image)
cv2.imshow("Compressed", image_comp)
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