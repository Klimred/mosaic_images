from PIL import Image
from config_values import *


# create an array of images from the unresized folder
def resize_images(standard_size, length):
    print(length)
    images = []
    for i in range(length):
        image = Image.open(f"{unresized_images_directory}/image ({i+1}).jpg")
        images.append(image)
    i = 1
    for image in images:
        image = image.resize((standard_size, standard_size))
        image = image.convert("RGB")
        image.save(f"{input_images_directory}/image ({i}).jpg", "JPEG")
        i += 1
    print("resized_images")

