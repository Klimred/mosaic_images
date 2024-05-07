from main import *
import matplotlib.pyplot as plt
# noinspection PyUnresolvedReferences
from mpl_toolkits.mplot3d import Axes3D


def color_distribution():
    target_image_cv2 = cv2.cvtColor(cv2.imread("./images/target_image/1.jpg"), cv2.COLOR_BGR2HSV)
    target_image_cv2 = cv2.resize(target_image_cv2, (64, 39))
    images, means = load_and_resize_images(input_images_directory, standard_size, num_files)

    h, s, v = cv2.split(target_image_cv2)
    # Flatten the arrays
    h = h.flatten()
    s = s.flatten()
    v = v.flatten()

    # Calculate the means of the hue, saturation, and value channels for all input images
    h_means = [np.mean(image[:, :, 0]) for image in images]
    s_means = [np.mean(image[:, :, 1]) for image in images]
    v_means = [np.mean(image[:, :, 2]) for image in images]

    # Create a figure with two subplots
    fig = plt.figure(figsize=(20, 10))

    # First subplot: target image
    ax1 = fig.add_subplot(121, projection='3d')
    scatter1 = ax1.scatter(h, s, v, c=v, cmap='viridis', alpha=0.5, rasterized=True)
    ax1.set_xlabel('Hue')
    ax1.set_ylabel('Saturation')
    ax1.set_zlabel('Value')
    ax1.set_title('Target Image')
    fig.colorbar(scatter1, ax=ax1)

    # Second subplot: means of input images
    ax2 = fig.add_subplot(122, projection='3d')
    scatter2 = ax2.scatter(h_means, s_means, v_means, c=v_means, cmap='viridis', alpha=0.5, rasterized=True)
    ax2.set_xlabel('Hue')
    ax2.set_ylabel('Saturation')
    ax2.set_zlabel('Value')
    ax2.set_title('Means of Input Images')
    fig.colorbar(scatter2, ax=ax2)

    plt.show()


