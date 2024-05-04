import datetime
import time

from image_to_np import image_to_np
from sklearn.cluster import MiniBatchKMeans
from PIL import Image
from sort_by_rgb import *
import os
from resize_images import resize_images
import cv2


# set to True if the images need to be resized to the standard size
resizing_needed = False
#the code doesn't like dark parts of the image, so we add a light boost to the pixel values
light_boost = -10

unresized_images_directory = "./images/unresized"
input_images_directory = "./images/cropped jpgs"

# change path to the image you want to convert
target_image = Image.open("./images/target_image/0.jpg")
# the original dimensions of the target image were 2048x1152
target_dimensions = (128, 72)
Image.MAX_IMAGE_PIXELS = 600000000
target_np = image_to_np(target_image, target_dimensions)

mosaic_images = []
standard_size = 90
out_path = "./out"


def count_files_in_directory(input_images_directory):
    return len([name for name in os.listdir(input_images_directory)
                if os.path.isfile(os.path.join(input_images_directory, name))])


num_files = count_files_in_directory(unresized_images_directory)


def load_and_resize_images(directory, standard_size, num_files):
    images = []
    means = []
    for i in range(num_files):
        image = cv2.cvtColor(cv2.imread(f"{directory}/image ({i+1}).jpg"), cv2.COLOR_BGR2RGB)
        resized_image = cv2.resize(image, (standard_size, standard_size))
        images.append(resized_image)
        means.append(np.mean(np.array(resized_image)))
    return images, means


def calculate_histogram(image, bins):
    # Reshape the image to a 3-dimensional array if necessary
    if image.ndim == 1:
        image = image.reshape(1, 1, 3)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    hist = cv2.calcHist([hsv_image], [0, 1, 2], None, [bins, bins, bins], [0, 180, 0, 256, 0, 256])
    cv2.normalize(hist, hist)
    return hist.flatten()


def load_and_calculate_histograms(directory, standard_size, num_files, bins):
    images = []
    histograms = []
    for i in range(num_files):
        image = cv2.cvtColor(cv2.imread(f"{directory}/image ({i+1}).jpg"), cv2.COLOR_BGR2RGB)
        resized_image = cv2.resize(image, (standard_size, standard_size))
        images.append(resized_image)
        histograms.append(calculate_histogram(resized_image, bins))
    return images, histograms


def find_fitting_image(target_pixel, images, histograms):
    target_hist = calculate_histogram(target_pixel, bins=len(histograms[0]))
    distances = [cv2.compareHist(target_hist, hist, cv2.HISTCMP_CHISQR) for hist in histograms]
    return images[np.argmin(distances)]


if resizing_needed:
    resize_images(standard_size, num_files)


# import all images to be used in the mosaic into an array
images, histograms = load_and_calculate_histograms(input_images_directory, standard_size, num_files, bins=[8, 8, 8])
print("Images loaded")

canvas = Image.new("RGB", (target_dimensions[0]*standard_size, target_dimensions[1]*standard_size), "white")
# Create chunks of the output image
for i in range(target_dimensions[0]):
    for j in range(target_dimensions[1]):
        target_pixel = target_np[i, j]
        fitting_image = find_fitting_image(target_pixel, images, histograms)
        pil_image = Image.fromarray(fitting_image)
        canvas.paste(pil_image, (i * standard_size, j * standard_size,))
    if i % 10 == 0:
        print(f"Column {i}/{target_dimensions[0]} took {time.time() - start_time} seconds")
        print(f"Finding the fitting image took {time_after_finding - time_before_finding} seconds")
        print(f"Pasting the image took: {time.time() - time_after_finding} seconds")
        print(f"Estimated time left: {(time.time() - start_time) * (target_dimensions[0] - i)} seconds")

# Save the processed image
current_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
canvas.save(f"{out_path}/mosaic_{current_date}.jpg")
print(f"Saved mosaic image as mosaic_{current_date}.jpg")


