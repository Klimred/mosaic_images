import datetime
import time

from PIL import Image
from sort_by_rgb import *
from color_distribution import *
import os
from resize_images import resize_images
import cv2
from scipy.spatial import KDTree

unresized_images_directory = "./images/unresized"
input_images_directory = "./images/cropped jpgs"


# the original dimensions of the target image were 2048x1152
dimension_presets = ((128, 72), (256, 144), (512, 288), (1024, 576), (2048, 1152))
target_dimensions = dimension_presets[2]
Image.MAX_IMAGE_PIXELS = 600000000

# get the target image and resize it to the target dimensions
target_image = cv2.imread("./images/target_image/1.jpg")
target_image = cv2.cvtColor(target_image, cv2.COLOR_BGR2HSV)
target_image = cv2.resize(target_image, target_dimensions)
target_image = target_image.transpose((1, 0, 2))

mosaic_images = []
standard_size = 30
out_path = "./out"


def count_files_in_directory(directory):
    return len([name for name in os.listdir(directory)
                if os.path.isfile(os.path.join(directory, name))])


def load_and_resize_images(directory, size, amount_of_files):
    images = []
    local_means = []
    for file in range(amount_of_files):
        image = cv2.cvtColor(cv2.imread(f"{directory}/image ({file + 1}).jpg"), cv2.COLOR_BGR2HSV)
        resized_image = cv2.resize(image, (size, size))
        images.append(resized_image)
        local_means.append(np.mean(resized_image, axis=(0, 1)))  # Calculate mean color for each image
    return images, local_means


def find_fitting_image(pixel, images, means_tree):
    _, index = means_tree.query(pixel)  # Find the nearest neighbor in the k-d tree
    closest_image = images[index]
    return cv2.cvtColor(closest_image, cv2.COLOR_HSV2RGB)  # Convert from HSV to RGB


def make_image():
    # import all images to be used in the mosaic into an array
    mosaic_images, means = load_and_resize_images(input_images_directory, standard_size, num_files)
    means_tree = KDTree(means)  # Create a k-d tree for the mean colors of the input images
    print("Images loaded")

    canvas = Image.new("RGB", (target_dimensions[0] * standard_size, target_dimensions[1] * standard_size), "white")
    # Create chunks of the output image
    for column in range(target_dimensions[0]):
        start_time = time.time()
        for row in range(target_dimensions[1]):
            time_begin = time.time()
            target_pixel = target_image[column, row]
            time_before_finding = time.time()
            fitting_image = find_fitting_image(target_pixel, mosaic_images, means_tree)
            time_after_finding = time.time()
            pil_image = Image.fromarray(fitting_image)
            canvas.paste(pil_image, (column * standard_size, row * standard_size,))
            if (column % 20 == 0) & (row == target_dimensions[1] - 1):
                print(f"Column {column}/{target_dimensions[0]} took {time.time() - start_time} seconds")
                print(f"Finding the fitting image took {time_after_finding - time_before_finding} seconds")
                print(f"Pasting the image took: {time.time() - time_after_finding} seconds")
                print(f"Estimated time left: {(time.time() - start_time) * (target_dimensions[0] - column)} seconds")

    # Save the processed image
    current_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    canvas.save(f"{out_path}/mosaic_{current_date}.jpg")
    print(f"Saved mosaic image as mosaic_{current_date}.jpg")


num_files = count_files_in_directory(unresized_images_directory)
# only run when the py is run directly
if __name__ == "__main__":
    input = input("r for resize, m for mosaic, d for distribution: ")
    if input == "r":
        resize_images(standard_size, num_files)
    elif input == "m" or " ":
        make_image()
    elif input == "d":
        color_distribution()

