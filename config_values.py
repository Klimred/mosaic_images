unresized_images_directory = "./images/unresized 2"
input_images_directory = "./images/cropped jpgs 2"
target_directory = "./images/target_image/1.jpg"

standard_size = 120
out_path = "./out"


# the original dimensions of the target image were 2048x1152
dimension_presets = ((128, 72), (256, 144), (512, 288), (1024, 576), (2048, 1152))
target_dimensions = dimension_presets[1]
