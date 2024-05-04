from PIL import Image


# create an array of images from the unresized folder
def resize_images(standard_size, length):
    print(length)
    images = []
    for i in range(length):
        image = Image.open(f"./images/unresized/image ({i+1}).jpg")
        images.append(image)
    i = 1
    for image in images:
        image = image.resize((standard_size, standard_size))
        image.save(f"./images/cropped jpgs/image ({i}).jpg")
        i += 1
    print("resized_images")

