import random
import os.path

from PIL import Image, ImageDraw
from collections import namedtuple

IMAGE_PATH = ''
IMAGE_TMP_PATHS = []

ImageData = namedtuple('ImageData', ['width', 'height', 'pixels'])


def tmp_images():
    global IMAGE_TMP_PATHS
    for i in range(3):
        IMAGE_TMP_PATHS.append(os.path.curdir + '/' + str(i) + '.jpg')
    return IMAGE_TMP_PATHS


def set_image_path(path):
    global IMAGE_PATH
    IMAGE_PATH = path


def open_image_file():
    image = Image.open(IMAGE_PATH)
    return image


def get_image_data(image):
    width = image.size[0]
    height = image.size[1]
    pixels = image.load()
    return ImageData(width, height, pixels)


def save_image_to_tmp_file():
    tmp_path = ''
    for path in IMAGE_TMP_PATHS:
        if not os.path.exists(path):
            tmp_path = path
            break
        else:
            tmp_path = IMAGE_TMP_PATHS[2]
    return tmp_path


def set_rgb_diapason(r, g, b):
    if r < 0:
        r = 0
    if g < 0:
        g = 0
    if b < 0:
        b = 0
    if r > 255:
        r = 255
    if g > 255:
        g = 255
    if b > 255:
        b = 255
    return r, g, b


def color_invert():
    image = open_image_file()
    image_data = get_image_data(image)
    draw = ImageDraw.Draw(image)
    for i in range(image_data.width):
        for j in range(image_data.height):
            a = image_data.pixels[i, j][0]
            b = image_data.pixels[i, j][1]
            c = image_data.pixels[i, j][2]
            draw.point((i, j), (255 - a, 255 - b, 255 - c))

    tmp_path = save_image_to_tmp_file()
    image.save(tmp_path, 'JPEG')
    del draw
    return tmp_path


def gray_scale():
    image = open_image_file()
    image_data = get_image_data(image)
    draw = ImageDraw.Draw(image)
    for i in range(image_data.width):
        for j in range(image_data.height):
            a = image_data.pixels[i, j][0]
            b = image_data.pixels[i, j][1]
            c = image_data.pixels[i, j][2]
            mid = (a + b + c) // 3
            draw.point((i, j), (mid, mid, mid))
    tmp_path = save_image_to_tmp_file()
    image.save(tmp_path, 'JPEG')
    del draw
    return tmp_path


def black_white():
    image = open_image_file()
    image_data = get_image_data(image)
    draw = ImageDraw.Draw(image)
    factor = 100
    for i in range(image_data.width):
        for j in range(image_data.height):
            a = image_data.pixels[i, j][0]
            b = image_data.pixels[i, j][1]
            c = image_data.pixels[i, j][2]
            sum_rgb = a + b + c
            if sum_rgb > (((255 + factor) // 2) * 3):
                a, b, c = 255, 255, 255
            else:
                a, b, c = 0, 0, 0
            draw.point((i, j), (a, b, c))
    tmp_path = save_image_to_tmp_file()
    image.save(tmp_path, 'JPEG')
    del draw
    return tmp_path


def sepia():
    image = open_image_file()
    image_data = get_image_data(image)
    draw = ImageDraw.Draw(image)
    depth = 50
    for i in range(image_data.width):
        for j in range(image_data.height):
            r = image_data.pixels[i, j][0]
            g = image_data.pixels[i, j][1]
            b = image_data.pixels[i, j][2]
            mid = (r + g + b) // 3
            r = mid + depth * 2
            g = mid + depth
            b = mid
            r, g, b = set_rgb_diapason(r, g, b)
            draw.point((i, j), (r, g, b))
    tmp_path = save_image_to_tmp_file()
    image.save(tmp_path, 'JPEG')
    del draw
    return tmp_path


def noise():
    image = open_image_file()
    image_data = get_image_data(image)
    draw = ImageDraw.Draw(image)
    factor = 100
    for i in range(image_data.width):
        for j in range(image_data.height):
            rand = random.randint(-factor, factor)
            r = image_data.pixels[i, j][0] + rand
            g = image_data.pixels[i, j][1] + rand
            b = image_data.pixels[i, j][2] + rand
            r, g, b = set_rgb_diapason(r, g, b)
            draw.point((i, j), (r, g, b))
    tmp_path = save_image_to_tmp_file()
    image.save(tmp_path, 'JPEG')
    del draw
    return tmp_path


def brightness(factor):
    image = open_image_file()
    image_data = get_image_data(image)
    draw = ImageDraw.Draw(image)
    for i in range(image_data.width):
        for j in range(image_data.height):
            r = image_data.pixels[i, j][0] + factor
            g = image_data.pixels[i, j][1] + factor
            b = image_data.pixels[i, j][2] + factor
            r, g, b = set_rgb_diapason(r, g, b)
            draw.point((i, j), (r, g, b))
    tmp_path = save_image_to_tmp_file()
    image.save(tmp_path, 'JPEG')
    del draw
    return tmp_path
