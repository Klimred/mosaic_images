from image_to_np import image_to_np
from PIL import Image
import os


def count_files_in_directory(path):
    return len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])


directory_path = './images/mosaic_images/'
num_files = count_files_in_directory(directory_path)

# change path to the image you want to convert
target_image = Image.open("./images/target_image/0.jpg")
target_dimensions = (2048, 1152)
target_np = image_to_np(target_image, target_dimensions)

input_images_directory = "./images/mosaic_images/"

# import all images to be used in the mosaic into an array
mosaic_images = []
for i in range(count_files_in_directory(input_images_directory)):
    image = Image.open(f"./images/mosaic_images/images/cropped jpgs/image ({i}).jpg")
    mosaic_images.append(image)


