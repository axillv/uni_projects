import cv2
import numpy as np
from matplotlib import pyplot as plt

def zonal_coding(blocks: list, num_coeff: int):
    """Keep the top num_coeff coefficients in each block and set the rest to zero,
    based on the variance of each coefficient position in all of the blocks

    Args:
    blocks: list of 32x32 blocks
    num_coeff: number of coefficients to keep

    Returns:
    list of 32x32 blocks
    """
    # calculate variance of each coefficient in all of the blocks
    variances = np.zeros(32*32)
    for i in range(32):
        for j in range(32):
            variances[i*32+j] = np.var([block[i,j] for block in blocks])

    # sort the variances in descending order
    sorted_variances = np.argsort(variances)[::-1]

    # set the rest of the coefficients to zero
    for i in range(num_coeff+1, 32*32):
        for block in blocks:
            block[sorted_variances[i]//32, sorted_variances[i]%32] = 0

    return blocks

def threshold_coding(blocks: list, num_coeff: int):
    """ Keep the top num_coeff coefficients in each block and set the rest to zero,
    based on the magnitude of each coefficient in each block

    Args:
    blocks: list of 32x32 blocks
    num_coeff: number of coefficients to keep

    Returns:
    list of 32x32 blocks
    """
    # for each block, keep the top num_coeff coefficients and set the rest to zero
    for block in blocks:
        sorted_indices = np.argsort(np.abs(block).flatten())[::-1]
        for i in range(num_coeff+1, 32*32):
            block[sorted_indices[i]//32, sorted_indices[i]%32] = 0
        
    return blocks

# load image
image = cv2.imread("img/lenna.jpg", cv2.IMREAD_GRAYSCALE)
# cut off the first row of the image
image = image[1:]
image = cv2.resize(image, (256,256))

# split image into 32x32 blocks
blocks = [image[i:i+32, j:j+32] 
          for i in range(0, image.shape[0], 32) 
          for j in range(0, image.shape[1], 32)]

# apply dct into each block
for i in range(len(blocks)):
    blocks[i] = np.float32(blocks[i]) / 255.0
    blocks[i] = cv2.dct(blocks[i])

# visualize a block using pyplot
plt.imshow(np.uint8(blocks[0]*255), cmap='gray')
plt.show()

blocks = threshold_coding(blocks, 128)

plt.imshow(np.uint8(blocks[0]*255), cmap='gray')
plt.show()

# apply inverse dct to get original image
for i in range(len(blocks)):
    blocks[i] = cv2.idct(blocks[i])
    blocks[i] = np.uint8(blocks[i]*255.0)

# transform blocks back into image
image_comp = np.zeros_like(image)
for i in range(0, len(blocks)):
    x = i // 8
    y = i % 8
    image_comp[x*32:x*32+32, y*32:y*32+32] = blocks[i]

# show original image and compressed in pyplot side by side
# plt.subplot(1, 2, 1)
# plt.imshow(image, cmap='gray')
# plt.title("Original")
# plt.subplot(1, 2, 2)
# plt.imshow(image_comp, cmap='gray')
# plt.title("Compressed")
# plt.show()
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