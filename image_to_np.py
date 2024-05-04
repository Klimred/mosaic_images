import numpy as np
from PIL import Image


def image_to_np(image, dimensions):
    # resize the image to fit the x,y dimensions
    image = image.resize(dimensions)
    img_array = np.array(image)
    # transpose to [x,y,rgb]
    img_array = np.transpose(img_array, (1, 0, 2))
