import os.path
import random
import tempfile
import shutil

from collections import namedtuple
from PIL import Image, ImageDraw

IMAGE_TMP_PATHS = []

ImageData = namedtuple('ImageData', ['width', 'height', 'pixels'])

IMAGE = ImageData(0, 0, [])


class TempFiles(object):
    def __init__(self, steps):
        self.TMP_FILES = []
        self.steps = steps
        self.temp_dir = ''

    def get_tmp_files(self):
        self.temp_dir = tempfile.mkdtemp()
        for i in range(self.steps):
            pre = 'tmp_{}'.format(i)
            temp = tempfile.NamedTemporaryFile(suffix='.jpg', prefix=pre, dir=self.temp_dir)
            self.TMP_FILES.append(temp)
        global IMAGE_TMP_PATHS
        IMAGE_TMP_PATHS = self.TMP_FILES
        return self.TMP_FILES

    def remove_tmp_dir(self):
        for path in self.TMP_FILES:
            path.close()
        shutil.rmtree(self.temp_dir, ignore_errors=True)


def set_image_data(path):
    image = Image.open(path)
    width = image.size[0]
    height = image.size[1]
    pixels = image.load()
    global IMAGE
    IMAGE = ImageData(width, height, pixels)


def save_image_to_tmp_file():
    pass


def set_rgb_diapason(r, g, b):
    r = min(max(r, 0), 255)
    g = min(max(g, 0), 255)
    b = min(max(b, 0), 255)
    return r, g, b


def get_image_size():
    w = IMAGE.width
    h = IMAGE.height
    return w, h


def prepare_new_file():
    new_image = Image.new('RGB', [IMAGE.width, IMAGE.height], (255, 255, 255))
    draw = ImageDraw.Draw(new_image)
    return new_image, draw


def color_invert():
    new_image, draw = prepare_new_file()
    for i in range(IMAGE.width):
        for j in range(IMAGE.height):
            a = IMAGE.pixels[i, j][0]
            b = IMAGE.pixels[i, j][1]
            c = IMAGE.pixels[i, j][2]
            draw.point((i, j), (255 - a, 255 - b, 255 - c))
    tmp_path = IMAGE_TMP_PATHS[0]
    new_image.save(tmp_path, 'JPEG')
    tmp_path.seek(0)
    del draw
    return os.path.abspath(tmp_path.name)


def gray_scale():
    new_image, draw = prepare_new_file()
    for i in range(IMAGE.width):
        for j in range(IMAGE.height):
            a = IMAGE.pixels[i, j][0]
            b = IMAGE.pixels[i, j][1]
            c = IMAGE.pixels[i, j][2]
            mid = (a + b + c) // 3
            draw.point((i, j), (mid, mid, mid))
    tmp_path = IMAGE_TMP_PATHS[0]
    new_image.save(tmp_path, 'JPEG')
    tmp_path.seek(0)
    del draw
    return os.path.abspath(tmp_path.name)


def black_white():
    new_image, draw = prepare_new_file()
    factor = 100
    for i in range(IMAGE.width):
        for j in range(IMAGE.height):
            a = IMAGE.pixels[i, j][0]
            b = IMAGE.pixels[i, j][1]
            c = IMAGE.pixels[i, j][2]
            sum_rgb = a + b + c
            if sum_rgb > (((255 + factor) // 2) * 3):
                a, b, c = 255, 255, 255
            else:
                a, b, c = 0, 0, 0
            draw.point((i, j), (a, b, c))
    tmp_path = IMAGE_TMP_PATHS[0]
    new_image.save(tmp_path, 'JPEG')
    tmp_path.seek(0)
    del draw
    return os.path.abspath(tmp_path.name)


def sepia():
    new_image, draw = prepare_new_file()
    depth = 50
    for i in range(IMAGE.width):
        for j in range(IMAGE.height):
            r = IMAGE.pixels[i, j][0]
            g = IMAGE.pixels[i, j][1]
            b = IMAGE.pixels[i, j][2]
            mid = (r + g + b) // 3
            r = mid + depth * 2
            g = mid + depth
            b = mid
            r, g, b = set_rgb_diapason(r, g, b)
            draw.point((i, j), (r, g, b))
    tmp_path = IMAGE_TMP_PATHS[0]
    new_image.save(tmp_path, 'JPEG')
    del draw
    return os.path.abspath(tmp_path.name)


def noise():
    new_image, draw = prepare_new_file()
    factor = 100
    for i in range(IMAGE.width):
        for j in range(IMAGE.height):
            rand = random.randint(-factor, factor)
            r = IMAGE.pixels[i, j][0] + rand
            g = IMAGE.pixels[i, j][1] + rand
            b = IMAGE.pixels[i, j][2] + rand
            r, g, b = set_rgb_diapason(r, g, b)
            draw.point((i, j), (r, g, b))
    tmp_path = IMAGE_TMP_PATHS[0]
    new_image.save(tmp_path, 'JPEG')
    del draw
    return os.path.abspath(tmp_path.name)


def brightness(factor):
    new_image, draw = prepare_new_file()
    for i in range(IMAGE.width):
        for j in range(IMAGE.height):
            r = IMAGE.pixels[i, j][0] + factor
            g = IMAGE.pixels[i, j][1] + factor
            b = IMAGE.pixels[i, j][2] + factor
            r, g, b = set_rgb_diapason(r, g, b)
            draw.point((i, j), (r, g, b))
    tmp_path = IMAGE_TMP_PATHS[0]
    new_image.save(tmp_path, 'JPEG')
    del draw
    return os.path.abspath(tmp_path.name)
