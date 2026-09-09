import cv2
import numpy as np
from matplotlib import pyplot as plt

image = cv2.imread("img/new_york.png", cv2.IMREAD_GRAYSCALE)

# apply gaussian filter to the image
image_blurred = cv2.GaussianBlur(image, (5,5), 1.75)
# apply gaussian white noise
noise = np.random.normal(0, 10, image.shape)
# calculate snr with variance and std
snr = 10 * np.log10(np.mean(image_blurred**2) / (np.var(noise) ** 2))
np.mean(image_blurred**2)print(f"SNR: {snr:.2f} dB")
image_noisy = image_blurred + noise
image_noisy = np.clip(image_noisy, 0, 255).astype(np.uint8)

# show two images
cv2.imshow("Original", image_blurred)
cv2.imshow("Noisy", image_noisy)
cv2.waitKey(0)