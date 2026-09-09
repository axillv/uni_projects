from PIL import Image

im = Image.open("img/leaf.jpg").convert("L")
# apply a threshold to the image
im = im.point(lambda p: p >= 220 and 255)

# apply moore boundary tracing algorithm
print(im.getpixel((0, 0)))

# pixels = list(im.getdata())
# width, height = im.size
# pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
# print(pixels)



im.show()