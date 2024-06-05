sample_type = 2
standard_size = 270
out_path = "./out"
target_number = 3
preset_to_use = 1
overlay_original_image = True
transparency_of_overlay = 0.5

unresized_images_directory = f"./images/unresized {sample_type}"
input_images_directory = f"./images/cropped jpgs {sample_type}"
target_directory = f"./images/target_image/{target_number}.jpg"


# the original dimensions of the target image were 2048x1152
dimension_presets = (128, 196, 256, 512, 1024)
target_dimensions = [0, 0]
target_dimensions[0] = dimension_presets[preset_to_use]
