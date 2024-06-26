import winsound

from config_values import *
import datetime
import time


from PIL import Image
import numpy as np
from color_distribution import *
import os
from resize_images import resize_images
import cv2
from scipy.spatial import KDTree

Image.MAX_IMAGE_PIXELS = 600000000


def load_target_image(index=0):
    global target_image
    target_directory = f"./images/target_image/{index}.jpg"
    target_image = cv2.imread(target_directory)
    target_image = cv2.cvtColor(target_image, cv2.COLOR_BGR2HSV)

    original_height, original_width = target_image.shape[:2]

    target_dimensions[0] = dimension_presets[preset_to_use]
    if original_width > original_height:
        target_dimensions[1] = int(target_dimensions[0] * original_height / original_width)
    else:
        target_dimensions[1] = int(target_dimensions[0] * original_width / original_height)
        target_dimensions[0], target_dimensions[1] = target_dimensions[1], target_dimensions[0]

    print (f"Target dimensions: {target_dimensions}")

    target_image = cv2.resize(target_image, tuple(target_dimensions))
    target_image = target_image.transpose((1, 0, 2))


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
            target_pixel = target_image[column, row]
            fitting_image = find_fitting_image(target_pixel, mosaic_images, means_tree)
            pil_image = Image.fromarray(fitting_image)
            canvas.paste(pil_image, (column * standard_size, row * standard_size,))
            if (column % 20 == 0) & (row == target_dimensions[1] - 1):
                print(f"Column {column}/{target_dimensions[0]} took {time.time() - start_time} seconds")
                print(f"Estimated time left: {(time.time() - start_time) * (target_dimensions[0] - column)} seconds")

    # Save the processed image
    current_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if overlay_original_image:
        print("Nearest neighbor mosaic image created, overlaying original image")
        target_image_pil = Image.fromarray(cv2.cvtColor(target_image.transpose((1, 0, 2)), cv2.COLOR_HSV2RGB))
        time_before_blend = time.time()
        canvas = Image.blend(canvas, target_image_pil.resize(canvas.size), alpha=0.5)
        end_time = time.time()
        print(f"Time to blend: {end_time - time_before_blend}")
    canvas.save(f"{out_path}/mosaic_{current_date}.jpg")
    # canvas.save(f"{out_path}/mosaic_{current_date}.png", "PNG")
    print(f"Saved mosaic image as mosaic_{current_date}.jpg")


num_files = count_files_in_directory(unresized_images_directory)
# only run when the py is run directly
if __name__ == "__main__":
    while True:
        load_target_image(target_number)
        userinput = input("r for resize, m for mosaic, d for distribution,\n "
                          "mult for multiple, q for quit: ")
        if userinput == "r":
            resize_images(standard_size, num_files)
        elif userinput == "m":
            make_image()
        elif userinput == "d":
            color_distribution()
        elif userinput == "mult":
            # parse two values, start and end
            start, end = map(int, input("Enter the start and end values separated by a space: ").split())
            for i in range(start, end+1):
                load_target_image(i)
                make_image()
        elif userinput == "q":
            break
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
