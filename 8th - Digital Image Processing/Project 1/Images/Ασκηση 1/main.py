import os

import cv2
import matplotlib.pyplot as plt
import numpy as np

# Change dynamic range to 0-255
with open("Images/Ασκηση 1/moon.jpg", "rb") as f:
    file_bytes = np.asarray(bytearray(f.read()), dtype=np.uint8)
img = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
if img is None:
    raise FileNotFoundError("Image not found. Check the path and filename.")

min_val_before = np.min(img)
max_val_before = np.max(img)
print(f"Dynamic range before: {min_val_before} - {max_val_before}")

img_fdr = (
    (img - min_val_before) * (255.0 / (max_val_before - min_val_before))
).astype(np.uint8)

min_val_after = np.min(img_fdr)
max_val_after = np.max(img_fdr)
print(f"Dynamic range after: {min_val_after} - {max_val_after}")

output_path = os.path.abspath("Images/Ασκηση 1/moon_fdr.jpg")
result, encoded_img = cv2.imencode(".jpg", img_fdr)
if result:
    with open(output_path, "wb") as f:
        f.write(encoded_img)
    print(f"Saving to: {output_path}, Success: True")
else:
    print(f"Saving to: {output_path}, Success: False")

# Calculate FFT and shifted FFT
fft_img = np.fft.fft2(img)
fft_img_magnitude = 20 * np.log(np.abs(fft_img) + 1)

fft_img_shifted = np.fft.fftshift(fft_img)
fft_img_shifted_magnitude = 20 * np.log(np.abs(fft_img_shifted) + 1)

# Save side-by-side comparison of FFT before and after shift
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.title("FFT (DC at [0,0])")
plt.imshow(fft_img_magnitude, cmap="gray")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.title("FFT (DC at center)")
plt.imshow(fft_img_shifted_magnitude, cmap="gray")
plt.axis("off")

plt.tight_layout()
plt.savefig(
    "Images/Ασκηση 1/moon_fft_compare.png", bbox_inches="tight", dpi=200
)
plt.close()
