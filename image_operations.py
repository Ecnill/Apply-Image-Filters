""" The different types of matrices used for different image filters. """
import os.path
import tempfile
from math import floor
import numpy as np
from PIL import Image, ImageDraw

import filters

IMAGE_PATH = ''
TEMP_FILE_PATH = ''


class TempFile:
    """ The file to save a temporary result of operations. """

    def __init__(self):
        self.file = tempfile.NamedTemporaryFile()
        self.temp_path = ''

    def create_temp_file(self):
        """ Creates the temporary file with the path. """
        self.temp_path = os.path.abspath(self.file.name)

    def close_temp_file(self):
        """ Closes the temporary file. """
        self.file.close()
        if os.path.exists(self.temp_path):
            os.remove(self.temp_path)


def setup_image_paths(path, temp_file):
    """
    Saves paths from the user's input.

    :param path: of the original image file.
    :param temp_file: the temporary result.
    """
    global IMAGE_PATH, TEMP_FILE_PATH
    IMAGE_PATH = path
    TEMP_FILE_PATH = temp_file


def get_image_data(path):
    """
    Gets a width, height, and pixes of the image.

    :param path: of the original image.
    :return: a width, height, and the pixels array of the image.
    """
    image = Image.open(path)
    width, height = image.size[0], image.size[1]
    return width, height, np.array(image)


def get_image_size():
    """
    Gets the image size.

    :return: the width and height of the image.
    """
    width, height, _ = get_image_data(IMAGE_PATH)
    return width, height


def color_invert():
    """ Inverts R,G,B of pixels: 255 - R, 255 - G, 255 - B. """
    global IMAGE_PATH
    _, _, pixels = get_image_data(IMAGE_PATH)
    red, green, blue = pixels[:, :, 0], pixels[:, :, 1], pixels[:, :, 2]
    pixels[:, :, 0] = 255 - red
    pixels[:, :, 1] = 255 - green
    pixels[:, :, 2] = 255 - blue
    IMAGE_PATH = TEMP_FILE_PATH
    Image.fromarray(pixels).save(TEMP_FILE_PATH, 'JPEG')


def gray_scale():
    """
    Ways for converting colors to grayscale:
    Average method: (R + G + B) / 3
    Lightness method: (max(R, G, B) + min(R, G, B)) / 2
    Luminosity method: 0.21 R + 0.72 G + 0.07 B
    """
    global IMAGE_PATH
    _, _, pixels = get_image_data(IMAGE_PATH)
    updated_pixels = np.copy(pixels).astype(int)
    red, green, blue = updated_pixels[:, :, 0], updated_pixels[:, :, 1], updated_pixels[:, :, 2]
    median = 0.21 * red + 0.72 * green + 0.07 * blue
    updated_pixels[:, :, 0], updated_pixels[:, :, 1], updated_pixels[:, :, 2] =\
        median, median, median
    updated_pixels = np.clip(updated_pixels[:, :, :], 0, 255)
    IMAGE_PATH = TEMP_FILE_PATH
    Image.fromarray(updated_pixels.astype('uint8')).save(TEMP_FILE_PATH, 'JPEG')


def sepia():
    """ Applies calculation with R,G,B of pixels to make the sepia effect. """
    global IMAGE_PATH
    _, _, pixels = get_image_data(IMAGE_PATH)
    updated_pixels = np.copy(pixels).astype(int)
    depth = 50
    red, green, blue = updated_pixels[:, :, 0], updated_pixels[:, :, 1], updated_pixels[:, :, 2]
    mid = (red + green + blue) // 3
    red, green, blue = mid + depth * 2, mid + depth, mid
    updated_pixels[:, :, 0], updated_pixels[:, :, 1], updated_pixels[:, :, 1] = red, green, blue
    updated_pixels = np.clip(updated_pixels[:, :, :], 0, 255)
    IMAGE_PATH = TEMP_FILE_PATH
    Image.fromarray(updated_pixels.astype('uint8')).save(TEMP_FILE_PATH, 'JPEG')


def noise():
    """ Applies the calculation with R,G,B of pixels to make the noise effect. """
    global IMAGE_PATH
    factor = 100
    width, height, pixels = get_image_data(IMAGE_PATH)
    updated_pixels = np.copy(pixels).astype(int)
    red, green, blue = updated_pixels[:, :, 0], updated_pixels[:, :, 1], updated_pixels[:, :, 2]
    rand = np.random.randint(-factor, factor, red.size).reshape(height, width)
    red, green, blue = red + rand, green + rand, blue + rand
    updated_pixels[:, :, 0], updated_pixels[:, :, 1], updated_pixels[:, :, 2] = red, green, blue
    updated_pixels = np.clip(updated_pixels[:, :, :], 0, 255)
    IMAGE_PATH = TEMP_FILE_PATH
    Image.fromarray(updated_pixels.astype('uint8')).save(TEMP_FILE_PATH, 'JPEG')


def brightness(factor):
    """


    :param factor:
    """
    global IMAGE_PATH
    _, _, pixels = get_image_data(IMAGE_PATH)
    updated_pixels = np.copy(pixels).astype(int)
    updated_pixels += factor
    updated_pixels = np.clip(updated_pixels[:, :, :], 0, 255)
    IMAGE_PATH = TEMP_FILE_PATH
    Image.fromarray(updated_pixels.astype('uint8')).save(TEMP_FILE_PATH, 'JPEG')


def blur():
    """ Applies the with R,G,B of pixels to make the sepia effect. """
    return apply_filter(filters.filter_blur)


def sharpen():
    """ Applies the with R,G,B of pixels to make the sharpen effect. """
    return apply_filter(filters.filter_sharpen)


def apply_filter(filter_matrix):
    """
    Helper method to apply the filter.

    :param filter_matrix: the matrix.
    """
    global IMAGE_PATH
    image = Image.open(IMAGE_PATH)
    width, height, pixels = image.size[0], image.size[1], image.load()
    new_image = Image.new('RGB', [width, height], (255, 255, 255))
    draw = ImageDraw.Draw(new_image)
    for x in range(width):
        for y in range(height):
            red, green, blue = 0.0, 0.0, 0.0

            for f_y in range(len(filter_matrix.filter)):
                for f_x in range(len(filter_matrix.filter[0])):
                    im_x = (x - len(filter_matrix.filter[0]) / 2 + f_x + width) % width
                    im_y = (y - len(filter_matrix.filter) / 2 + f_y + height) % height

                    red += pixels[im_x, im_y][0] * filter_matrix.filter[f_y][f_x]
                    green += pixels[im_x, im_y][1] * filter_matrix.filter[f_y][f_x]
                    blue += pixels[im_x, im_y][2] * filter_matrix.filter[f_y][f_x]

            red = min(max(int(filter_matrix.factor * red + filter_matrix.bias), 0), 255)
            green = min(max(int(filter_matrix.factor * green + filter_matrix.bias), 0), 255)
            blue = min(max(int(filter_matrix.factor * blue + filter_matrix.bias), 0), 255)
            draw.point((x, y), (red, green, blue))
            print('Applying filter {}... '.format(filter_matrix.name)
                  + str(floor((x * height + y) / (width * height) * 100)) + '%  ', end='\r')

    new_image.save(TEMP_FILE_PATH, 'JPEG')
    IMAGE_PATH = TEMP_FILE_PATH
    del draw
