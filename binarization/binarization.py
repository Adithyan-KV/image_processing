import numpy as np
from PIL import Image


def binarize(file_path):
    with Image.open(file_path) as image:
        image_data = np.asarray(image)
        preprocessed_image_data = preprocess_image(image_data)
        grayscale_image = Image.fromarray(preprocessed_image_data)
        grayscale_image.show()


def preprocess_image(image_data):
    num_channels = image_data.shape[2]
    # weights chosen from https://en.wikipedia.org/wiki/Luma_(video)
    channel_weight_matrix = np.array([0.3, 0.59, 0.11])
    if num_channels == 1:
        grayscale_image = image_data
    elif num_channels == 3:
        grayscale_image = np.matmul(image_data, channel_weight_matrix)
    elif num_channels == 4:
        color_channel_data = image_data[:, :, :3]
        grayscale_image = np.matmul(color_channel_data, channel_weight_matrix)
    return grayscale_image


if __name__ == "__main__":
    binarize('test_images/bridge.jpg')
