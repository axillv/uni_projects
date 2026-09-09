import cv2
import numpy as np

def add_gaussian_noise(image, mean=0, std_dev=1, weight=1):
    # Returns numpy array
    noise = np.random.normal(mean, std_dev, image.shape).astype(np.uint8)
    # https://stackoverflow.com/questions/40119743/convert-a-grayscaleimage-to-a-3-channel-image

    # back to 3 channel
    #noise = np.stack((noise,)*3, axis=-1)
    noise = noise * weight
    # Convert the noise array to the same data type as the image
    noise = noise.astype(image.dtype)
    noisy_image = cv2.add(image, noise)
    return noisy_image

def SNR(image, noisy_image):
    # Signal to Noise Ratio (SNR)
    # https://en.wikipedia.org/wiki/Signal-to-noise_ratio_(imaging)

    # mean of the squared pixel values of the original image
    signal_power = np.mean(image ** 2)
    # mean of the squared pixel values of the noise image (noisy - original)
    noise_power = np.mean((image - noisy_image) ** 2)
    # (dB) = 10 * log10(Psignal/Pnoise)
    return 10 * np.log10(signal_power / noise_power)

# 1. Additive Gaussian
image = cv2.imread('img/board.png', cv2.IMREAD_GRAYSCALE)
assert image is not None, "File could not be read, check with os.path.exists()"
gaussian_noisy_image = add_gaussian_noise(image, 0, 0.53, 1)
print(f'SNR with gaussian noise: {SNR(image, gaussian_noisy_image)}')