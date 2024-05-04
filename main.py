from image_to_np import image_to_np
from PIL import Image
from sort_by_rgb import *
import os
from resize_images import resize_images
import cv2


# set to True if the images need to be resized to the standard size
resizing_needed = False


def count_files_in_directory(input_images_directory):
    return len([name for name in os.listdir(input_images_directory)
                if os.path.isfile(os.path.join(input_images_directory, name))])


def load_and_resize_images(directory, standard_size, num_files):
    images = []
    means = []
    for i in range(num_files):
        image = cv2.cvtColor(cv2.imread(f"{directory}/image ({i+1}).jpg"), cv2.COLOR_BGR2RGB)
        resized_image = cv2.resize(image, (standard_size, standard_size))
        images.append(resized_image)
        means.append(np.mean(np.array(resized_image)))
    return images, means


def find_fitting_image(target_pixel, images):
    closest_image = None
    closest_distance = float("inf")
    for image in images:
        distance = np.linalg.norm(target_pixel - np.mean(image))
        if distance < closest_distance:
            closest_distance = distance
            closest_image = image
    return closest_image

unresized_images_directory = "./images/unresized"
input_images_directory = "./images/cropped jpgs"
num_files = count_files_in_directory(unresized_images_directory)

# change path to the image you want to convert
target_image = Image.open("./images/target_image/0.jpg")
# the original dimensions of the target image were 2048x1152
target_dimensions = (512, 288)
Image.MAX_IMAGE_PIXELS = 600000000
target_np = image_to_np(target_image, target_dimensions)

mosaic_images = []
standard_size = 450
out_path = "./out"
if resizing_needed:
    resize_images(standard_size, num_files)

# let's chunk it out
chunk_size = 64
chunks_horizontal = target_dimensions[0] // chunk_size
chunks_vertical = target_dimensions[1] // chunk_size

# import all images to be used in the mosaic into an array
mosaic_images, means = load_and_resize_images(input_images_directory, standard_size, num_files)
print("Images loaded")

# Create chunks of the output image
for i in range(chunks_horizontal):
    for j in range(chunks_vertical):
        # Create a new canvas for the chunk
        chunk_canvas = Image.new("RGB", (chunk_size*standard_size, chunk_size*standard_size), "white")
        print(f"Processing chunk {i}_{j}")
        # Process the chunk as before
        for x in range(chunk_size):
            print(f"Processing chunk {i}_{j} {x}/{chunk_size}")
            for y in range(chunk_size):
                target_pixel = target_np[i*chunk_size + x, j*chunk_size + y]
                fitting_image = find_fitting_image(target_pixel, mosaic_images)
                pil_image = Image.fromarray(cv2.cvtColor(fitting_image, cv2.COLOR_BGR2RGB))
                chunk_canvas.paste(pil_image, (x * standard_size, y * standard_size,))

        # Save the processed chunk as a separate image
        chunk_canvas.save(f"{out_path}/chunk_{i}_{j}.jpg")
    print(f"Saved chunk {i}_{j}")


