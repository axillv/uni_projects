import cv2
import numpy as np
import matplotlib.pyplot as plt

def moving_average(size: int, img: np.ndarray) -> np.ndarray:
    kernel = np.ones((size, size), np.float32) / (size ** 2)
    return cv2.filter2D(img, -1, kernel)

def median_filter(size: int, img: np.ndarray) -> np.ndarray:
    return cv2.medianBlur(img, size)

board = cv2.imread('img/board.png', cv2.IMREAD_GRAYSCALE)

noise = np.random.normal(0, 8, board.shape)
board_noisy = board + noise
board_noisy = np.clip(board_noisy, 0, 255).astype(np.uint8)
snr = 10 * np.log10(np.mean(board) / np.std(noise))
print(f'SNR: {snr:.2f}dB')


average_boards = []
median_boards = []
# loop over the sizes of the filters, add them to a plot and show them all at once
for size in range(3,10):
    average_boards.append(moving_average(size, board_noisy))

    if size%2 == 1:
        median_boards.append(median_filter(size, board_noisy))
    
# show all images one by one, resize to 1920x1080
# for i in range(len(average_boards)):
#     cv2.imshow(f'Average filter size {i*2+3}', average_boards[i])

# for i in range(len(median_boards)):
#     cv2.imshow(f'Median filter size {i*2+3}', median_boards[i])

cv2.imshow('Original', board)
cv2.imshow('Noisy', board_noisy)
cv2.waitKey(0)
