import math

import cv2
import matplotlib.pyplot as plt
import numpy as np

# Load the image
image = cv2.imread('img/hallway.png', cv2.IMREAD_GRAYSCALE)

# use sobel mask to find x and y gradients
sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)

# convert the gradients to absolute values
sobel_x = np.uint8(np.absolute(sobel_x))
sobel_y = np.uint8(np.absolute(sobel_y))
sobel_combined = cv2.bitwise_or(sobel_x, sobel_y)

# show the images
# cv2.imshow('Original', image)
# cv2.imshow('Sobel X', sobel_x)
# cv2.imshow('Sobel Y', sobel_y)
# cv2.waitKey(0)

# Show combined along with histogram
# plt.figure(figsize=(10, 5))
# plt.subplot(1, 2, 1)
# plt.imshow(sobel_combined, cmap='gray')
# plt.title('Sobel Combined')
# plt.axis('off')

# plt.subplot(1, 2, 2)
# plt.hist(sobel_combined.ravel(), 256, [0, 256])
# plt.title('Histogram')
# plt.show()

# apply thresholding to combined
_, sobel_combined_thresh16 = cv2.threshold(sobel_combined, 16, 255, cv2.THRESH_BINARY)
_, sobel_combined_thresh32 = cv2.threshold(sobel_combined, 32, 255, cv2.THRESH_BINARY)
_, sobel_combined_thresh48 = cv2.threshold(sobel_combined, 48, 255, cv2.THRESH_BINARY)

# Show combined
# cv2.imshow('Sobel Combined16', sobel_combined_thresh16)
# cv2.imshow('Sobel Combined32', sobel_combined_thresh32)
# cv2.imshow('Sobel Combined48', sobel_combined_thresh48)
# cv2.waitKey(0)

# apply hough transform to find lines
lines = cv2.HoughLinesP(sobel_combined_thresh48, 1, np.pi / 180, 150, minLineLength=15, maxLineGap=1)
#change image to bgr
image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

# lines = cv2.HoughLines(sobel_combined_thresh48, 1, np.pi / 180, 50)
# #change image to bgr
# image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

# if lines is not None:
#     for i in range(0, len(lines)):
#         rho = lines[i][0][0]
#         theta = lines[i][0][1]
#         a = math.cos(theta)
#         b = math.sin(theta)
#         x0 = a * rho
#         y0 = b * rho
#         pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
#         pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
#         cv2.line(image, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)

# resize
image = cv2.resize(image, (960, 540))
cv2.imshow('Hough Lines', image)
cv2.waitKey(0)



