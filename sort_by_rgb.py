from PIL import Image
import numpy as np


# create a function that uses quicksort to use pointers and sort the images by the amount of red
def sort_by_red(images):
    # create a list of tuples, each containing the red value and the image reference
    red_values = [(sum(image.getdata(0)), image) for image in images]

    # sort the list of tuples by the red value (first element of each tuple)
    red_values.sort(key=lambda x: x[0])

    # now red_values is sorted by red value, and for each red value you have the corresponding image
    return red_values


def sort_by_green(images):
    # create a list of tuples, each containing the green value and the image reference
    green_values = [(sum(image.getdata(1)), image) for image in images]

    # sort the list of tuples by the green value (first element of each tuple)
    green_values.sort(key=lambda x: x[0])

    # now red_values is sorted by green value, and for each red value you have the corresponding image
    return green_values


def sort_by_blue(images):
    # create a list of tuples, each containing the blue value and the image reference
    blue_values = [(sum(image.getdata(2)), image) for image in images]

    # sort the list of tuples by the blue value (first element of each tuple)
    blue_values.sort(key=lambda x: x[0])

    # now red_values is sorted by blue value, and for each red value you have the corresponding image
    return blue_values


def sort_by_brightness(images):
    # create a list of tuples, each containing the brightness value and the image reference
    brightness_values = [(sum(image.getdata()), image) for image in images]

    # sort the list of tuples by the brightness value (first element of each tuple)
    brightness_values.sort(key=lambda x: x[0])

    # now red_values is sorted by brightness value, and for each red value you have the corresponding image
    return brightness_values


def red_green_blue_brightness(images):
    return sort_by_red(images), sort_by_green(images), sort_by_blue(images), sort_by_brightness(images)
