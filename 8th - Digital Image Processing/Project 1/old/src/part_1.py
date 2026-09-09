from enum import Enum

import cv2
import numpy as np
import matplotlib.pyplot as plt

class MooreDirection(Enum):
    West = 0
    NW = 1
    North = 2
    NE = 3
    East = 4
    SE = 5
    South = 6
    SW = 7

def map_direction(direction: MooreDirection) -> tuple[int, int]:
    return {
        MooreDirection.West: (0, -1),
        MooreDirection.NW: (-1, -1),
        MooreDirection.North: (-1, 0),
        MooreDirection.NE: (-1, 1),
        MooreDirection.East: (0, 1),
        MooreDirection.SE: (1, 1),
        MooreDirection.South: (1, 0),
        MooreDirection.SW: (1, -1)
    }[direction]

def moore_tracing(image: cv2.typing.MatLike) -> list[tuple[int, int]]:
    # create lambda function for adding coordinate tuples
    add_coords = lambda a, b: (a[0] + b[0], a[1] + b[1])

    # Find the topmost leftmost black pixel
    # remember, coordinates are (height, width)
    height, width = image.shape
    for x in range(width):
        for y in range(height):
            if image[y,x] == 0:
                b0 = (y,x)
                break

    b = [b0]
    # set c0 as the west neighbor of b0
    c_direction = MooreDirection.West
    c = add_coords(b0, map_direction(c_direction))
    

    while True:
        # Check if c is black
        c = add_coords(b[-1], map_direction(c_direction))
        if image[c] != 0:
            # c is white, rotate c_direction clockwise
            c_direction = MooreDirection((c_direction.value + 1) % 8)
            c = add_coords(b[-1], map_direction(c_direction))
            continue

        # Black pixel found, add it to the boundary, set c as nk-1
        b.append(c)

        # check if returned to b0
        if c == b0:
            break

        c_direction = MooreDirection((c_direction.value - 1) % 8)
        c = add_coords(b[-1], map_direction(c_direction))
    
    # return width, height instead of height, width to use with drawcontour
    return [(point[1], point[0]) for point in b]
    
if __name__ == "__main__":
    leaf = cv2.imread("img/leaf.jpg")
    leaf_grayscale = cv2.cvtColor(leaf, cv2.COLOR_BGR2GRAY)
    _, leaf_binary = cv2.threshold(leaf_grayscale, 220, 255, cv2.THRESH_BINARY)

    b = moore_tracing(leaf_binary)
    contour = np.array(b).reshape((-1,1,2)).astype(np.int32)
    cv2.drawContours(leaf, contour, -1, (0,0,255), 2)

    leaf_moore_processing_horizontal = np.concatenate((cv2.cvtColor(leaf_grayscale, cv2.COLOR_GRAY2BGR), 
                                                    cv2.cvtColor(leaf_binary, cv2.COLOR_GRAY2BGR),
                                                    leaf), axis=1)

    # cv2.imshow("Leaf Moore Processing", leaf_moore_processing_horizontal)
    # cv2.waitKey(0)

    # Fourier Descriptors
    contour_array = contour[:, 0, :]
    contour_complex = np.empty(contour_array.shape[:-1], dtype=complex)
    contour_complex.real = contour_array[:, 0]
    contour_complex.imag = contour_array[:, 1]
    fourier_result = np.fft.fftshift(np.fft.fft(contour_complex))
    magnitude_spectrum = 20*np.log(np.abs(fourier_result))

    # plt.plot(magnitude_spectrum)
    # plt.show()

    # apply low pass to the fourier result
    trash_percent = 0.99
    desc_to_trash = int(trash_percent * len(fourier_result))
    fourier_result[:desc_to_trash//2] = 0
    fourier_result[-desc_to_trash//2:] = 0
    magnitude_spectrum = 20*np.log(np.abs(fourier_result))
    # plt.plot(magnitude_spectrum)

    # plt.show()


    f_ishift = np.fft.ifftshift(fourier_result)
    img_back = np.fft.ifft(f_ishift)
    # turn the complex number into real number coordinates for the image contour
    img_back = np.array([img_back.real, img_back.imag]).T
    img_back = img_back.reshape((-1,1,2)).astype(np.int32)
    leaf_fourier = cv2.imread("img/leaf.jpg")
    cv2.drawContours(leaf_fourier, img_back, -1, (0,0,255), 2)
    cv2.imshow("Fourier", leaf_fourier)
    cv2.waitKey(0)
    # cv2.imshow("Fourier", img_back)


