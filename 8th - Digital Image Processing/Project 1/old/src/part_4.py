import cv2
import matplotlib.pyplot as plt
import numpy as np

def plot_img_and_hist(images: list[np.ndarray], title: str = "Plot"):
    """Plot images and their histograms in a 2x3 grid.
    
    Args:
        images (list[np.ndarray]): List of images to plot.
        title (str, optional): Title of the plot. Defaults to "Plot".
    """
    # Calculate histogram for each image
    hist = []
    for img in images:
        hist.append(cv2.calcHist([img], [0], None, [256], [0, 256]))

    plt.figure(figsize=(10, 6))

    for i, img in enumerate(images, start=1):
        plt.subplot(2, 3, i)
        plt.imshow(img, cmap='gray')
        plt.title(f'Image {i}')
        plt.axis('off')
    
    for i, h in enumerate(hist, start=4):
        plt.subplot(2, 3, i)
        plt.plot(h, color='black')
        plt.title(f'Histogram {i-3}')
        plt.xlabel('Pixel value')
        plt.ylabel('Frequency')

    plt.suptitle(title)
    plt.tight_layout()
    plt.show()

def apply_local_histogram_equalization(images: list[np.ndarray], grid_size: int) -> list[np.ndarray]:
    """Apply local histogram equalization to each image in the list.
    
    Args:
        images (list[np.ndarray]): List of images to apply local histogram equalization.
    
    Returns:
        list[np.ndarray]: List of images after applying local histogram equalization.
    """
    images_local_eq = []
    for img in images:
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(grid_size, grid_size))
        img_eq = clahe.apply(img)
        images_local_eq.append(img_eq)
    
    return images_local_eq

if __name__ == "__main__":
    # 1.Load Original Images
    images = []
    for i in range(1, 4):
        img = cv2.imread(f'img/dark_road_{i}.jpg', cv2.IMREAD_GRAYSCALE)
        images.append(img)

    # plot_img_and_hist(images, "Original Images")

    # 2.Apply global histogram equalization to each image
    images_global_eq = []
    for img in images:
        img_eq = cv2.equalizeHist(img)
        images_global_eq.append(img_eq)

    # plot_img_and_hist(images_global_eq, "Global Histogram Equalization")

    # 3.Apply local histogram equalization to each image
    images_local_eq_3 = apply_local_histogram_equalization(images, 3)
    images_local_eq_5 = apply_local_histogram_equalization(images, 5)
    images_local_eq_7 = apply_local_histogram_equalization(images, 7)

    
    # plot_img_and_hist(images_local_eq, "Local Histogram Equalization")

    # Show local eq images side by side, by concatting them
    for i in range(3):
        img_concat = np.concatenate((images_local_eq_3[i], images_local_eq_5[i], images_local_eq_7[i]), axis=0)
        cv2.imshow(f'Local Histogram Equalization Image {i+1}', img_concat)
    
    cv2.waitKey(0)

## ΤΟ 5 ΕΙΝΑΙ ΕΝΑ 