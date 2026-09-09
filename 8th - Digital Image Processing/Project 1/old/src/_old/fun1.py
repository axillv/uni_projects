from PIL import Image

def topleft_black_pixel( image: Image.Image) -> tuple[int, int]:
    """
    Returns the location of the uppermost leftmost black pixel in the image
    
    Args:
        image (Image.Image): The image to be processed.
        
    Returns:
        tuple: The uppermost leftmost location of the image.
    """

    width, height = image.size
    for y in range(height):
        for x in range(width):
            if image.getpixel((x, y)) == 0:
                return (x, y)
    return None

def next_clockwise_pixel(image: Image.Image, 
                         current_pixel: tuple[int, int], 
                         previous_pixel: tuple[int, int]
                         ) -> tuple[int, int]:
    """
    Returns the next clockwise pixel location from the current pixel

    Args:
        image (Image.Image): The image to be processed.
        current_pixel (tuple): The current pixel location. (b)
        previous_pixel (tuple): The previous pixel location. (c)

    Returns:
        tuple: The next clockwise pixel location.
    """
    x, y = current_pixel
    x1, y1 = previous_pixel
    width, height = image.size





def moore_tracing(image: Image.Image):
    
    b0 = topleft_black_pixel(image)
    # set c0 as the west neighbor of b0
    c0 = b0 - (1, 0) # (x, y): width, height

    
    