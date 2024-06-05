import concurrent.futures
from PIL import Image
from config_values import *


def resize_image(i, standard_size):
    image = Image.open(f"{unresized_images_directory}/image ({i+1}).jpg")
    image = image.resize((standard_size, standard_size))
    image = image.convert("RGB")
    image.save(f"{input_images_directory}/image ({i+1}).jpg", "JPEG")


def resize_images(standard_size, length):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(resize_image, range(length), [standard_size]*length)
    print("resized_images")
