import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def binarize(file_path):
    with Image.open(file_path) as image:
        image_data = np.asarray(image)
        grayscale_image_data = preprocess_image(image_data)
        # binarized_image_data = otsu_binarize(grayscale_image_data)
        binarized_image_data = localized_otsu_binarize(grayscale_image_data)
        binarized_image = Image.fromarray(np.uint8(binarized_image_data))
        binarized_image.save('bin_handwriting.png')


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


def otsu_binarize(image_data):
    optimal_threshold = get_optimal_threshold(image_data)
    # generate_histogram(image_data, optimal_threshold)
    binarized_image = (image_data > optimal_threshold) * 255
    return binarized_image


def localized_otsu_binarize(image_data):
    segment = 20
    rows, columns = image_data.shape
    bin_image = np.zeros_like(image_data)
    for row in range(0, rows, segment):
        for column in range(0, columns, segment):
            if abs(rows - row) < segment:
                if abs(columns - column) < segment:
                    thr = get_optimal_threshold(image_data[row:, column:])
                    bin_image[row:, column:] = image_data[row:, column:] > thr
            elif abs(columns - column) < segment:
                thr = get_optimal_threshold(
                    image_data[row:row + segment, column:])
                bin_image[row:row + segment,
                          column:] = (image_data[row: row + segment, column:] > thr)
            else:
                thr = get_optimal_threshold(
                    image_data[row: row + segment, column: column + segment])
                bin_image[row: row + segment, column: column + segment] = (
                    image_data[row: row + segment, column: column + segment] > thr)
    binarized_image = bin_image * 255
    return binarized_image


def get_optimal_threshold(image_data):
    btw_class_variances = np.zeros(256)
    for threshold in range(256):
        total_pixel_count = image_data.size
        w_1 = (image_data <= threshold).sum() / total_pixel_count
        w_2 = 1 - w_1
        if w_1 == 0 or w_2 == 0:
            btw_class_variances[threshold] = 0
        else:
            mean_1 = np.mean(image_data[image_data <= threshold])
            mean_2 = np.mean(image_data[image_data > threshold])
            variance = w_1 * w_2 * (mean_1 - mean_2)**2
            btw_class_variances[threshold] = variance

    optimal_threshold = np.argmax(btw_class_variances)
    return optimal_threshold


def generate_histogram(image_data, threshold):
    counts, bins = np.histogram(image_data, range(0, 255))
    plt.bar(bins[: -1], counts, width=1)
    plt.axvline(threshold, color='black')
    plt.xlabel('intensity')
    plt.ylabel('freq of pixels')
    plt.savefig('handwriting_hist.png', dpi=300)
    plt.show()


if __name__ == "__main__":
    binarize('test_images/handwriting.jpg')
