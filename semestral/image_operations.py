import os.path
import tempfile
import numpy as np
from PIL import Image, ImageDraw
from math import floor

import filters

IMAGE_PATH = ''
TEMP_FILE_PATH = ''


class TempFile:
    def __init__(self):
        self.temp_path = ''

    def create_temp_file(self):
        self.file = tempfile.NamedTemporaryFile()
        self.temp_path = os.path.abspath(self.file.name)

    def close_temp_file(self):
        self.file.close()
        if os.path.exists(self.temp_path):
            os.remove(self.temp_path)


def send_image_from_gui(path, temp_file):
    global IMAGE_PATH, TEMP_FILE_PATH
    IMAGE_PATH = path
    TEMP_FILE_PATH = temp_file


def get_image_data(path):
    image = Image.open(path)
    w, h = image.size[0], image.size[1]
    return w, h, np.array(image)


def get_image_size():
    w, h, _ = get_image_data(IMAGE_PATH)
    return w, h


def color_invert():
    global IMAGE_PATH
    _, _, pix = get_image_data(IMAGE_PATH)
    r, g, b = pix[:, :, 0], pix[:, :, 1], pix[:, :, 2]
    pix[:, :, 0] = 255 - r
    pix[:, :, 1] = 255 - g
    pix[:, :, 2] = 255 - b
    IMAGE_PATH = TEMP_FILE_PATH
    Image.fromarray(pix).save(TEMP_FILE_PATH, 'JPEG')


def gray_scale():
    """  Ways for converting colors to grayscale:
        Average method: (R + G + B) / 3
        Lightness method: (max(R, G, B) + min(R, G, B)) / 2
        Luminosity method: 0.21 R + 0.72 G + 0.07 B """
    global IMAGE_PATH
    _, _, p = get_image_data(IMAGE_PATH)
    pix = np.copy(p).astype(int)
    r, g, b = pix[:, :, 0], pix[:, :, 1], pix[:, :, 2]
    m = 0.21 * r + 0.72 * g + 0.07 * b
    pix[:, :, 0], pix[:, :, 1], pix[:, :, 2] = m, m, m
    pix = np.clip(pix[:, :, :], 0, 255)
    IMAGE_PATH = TEMP_FILE_PATH
    Image.fromarray(pix.astype('uint8')).save(TEMP_FILE_PATH, 'JPEG')


def sepia():
    global IMAGE_PATH
    _, _, p = get_image_data(IMAGE_PATH)
    pix = np.copy(p).astype(int)
    depth = 50
    r, g, b = pix[:, :, 0], pix[:, :, 1], pix[:, :, 2]
    mid = (r + g + b) // 3
    r, g, b = mid + depth * 2, mid + depth, mid
    pix[:, :, 0], pix[:, :, 1] , pix[:, :, 1] = r, g, b
    pix = np.clip(pix[:, :, :], 0, 255)
    IMAGE_PATH = TEMP_FILE_PATH
    Image.fromarray(pix.astype('uint8')).save(TEMP_FILE_PATH, 'JPEG')


def noise():
    global IMAGE_PATH
    factor = 100
    w, h, p = get_image_data(IMAGE_PATH)
    pix = np.copy(p).astype(int)
    r, g, b = pix[:, :, 0], pix[:, :, 1], pix[:, :, 2]
    rand = np.random.randint(-factor, factor, r.size).reshape(h, w)
    r, g, b = r + rand,  g + rand, b + rand
    pix[:, :, 0], pix[:, :, 1], pix[:, :, 2] = r, g, b
    pix = np.clip(pix[:, :, :], 0, 255)
    IMAGE_PATH = TEMP_FILE_PATH
    Image.fromarray(pix.astype('uint8')).save(TEMP_FILE_PATH, 'JPEG')


def brightness(factor):
    global IMAGE_PATH
    w, h, p = get_image_data(IMAGE_PATH)
    pix = np.copy(p).astype(int)
    pix += factor
    pix = np.clip(pix[:, :, :], 0, 255)
    IMAGE_PATH = TEMP_FILE_PATH
    Image.fromarray(pix.astype('uint8')).save(TEMP_FILE_PATH, 'JPEG')


def blur():
    return apply_filter(filters.filter_blur)


def sharpen():
    return apply_filter(filters.filter_sharpen)


def apply_filter(filter_matrix):
    global IMAGE_PATH
    image = Image.open(IMAGE_PATH)
    w, h, p = image.size[0], image.size[1], image.load()
    new_image = Image.new('RGB', [w, h], (255, 255, 255))
    draw = ImageDraw.Draw(new_image)
    for x in range(w):
        for y in range(h):
            r, g, b = 0.0, 0.0, 0.0

            for fy in range(len(filter_matrix.filter)):
                for fx in range(len(filter_matrix.filter[0])):

                    im_x = (x - len(filter_matrix.filter[0]) / 2 + fx + w) % w
                    im_y = (y - len(filter_matrix.filter) / 2 + fy + h) % h

                    r += p[im_x, im_y][0] * filter_matrix.filter[fy][fx]
                    g += p[im_x, im_y][1] * filter_matrix.filter[fy][fx]
                    b += p[im_x, im_y][2] * filter_matrix.filter[fy][fx]

            r = min(max(int(filter_matrix.factor * r + filter_matrix.bias), 0), 255)
            g = min(max(int(filter_matrix.factor * g + filter_matrix.bias), 0), 255)
            b = min(max(int(filter_matrix.factor * b + filter_matrix.bias), 0), 255)
            draw.point((x, y), (r, g, b))
            print('Applying filter {}... '.format(filter_matrix.name)
                  + str(floor((x * h + y) / (w * h) * 100)) + '%  ', end='\r')

    new_image.save(TEMP_FILE_PATH, 'JPEG')
    IMAGE_PATH = TEMP_FILE_PATH
    del draw
