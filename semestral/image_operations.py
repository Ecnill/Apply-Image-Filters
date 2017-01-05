import random


from PIL import Image, ImageDraw
from collections import namedtuple

IMAGE_PATH = ''


ImageData = namedtuple('ImageData', ['width', 'height', 'pixels'])


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
    image.save("src/result_invert.jpg", "JPEG")
    del draw


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
    image.save("src/result_gray.jpg", "JPEG")
    del draw


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
    image.save("src/result_bw.jpg", "JPEG")
    del draw


def sepia():
    image = open_image_file()
    image_data = get_image_data(image)
    draw = ImageDraw.Draw(image)
    depth = 50
    for i in range(image_data.width):
        for j in range(image_data.height):
            a = image_data.pixels[i, j][0]
            b = image_data.pixels[i, j][1]
            c = image_data.pixels[i, j][2]
            mid = (a + b + c) // 3
            a = mid + depth * 2
            b = mid + depth
            c = mid
            if a > 255:
                a = 255
            if b > 255:
                b = 255
            if c > 255:
                c = 255
            draw.point((i, j), (a, b, c))
    image.save("src/result_sepia.jpg", "JPEG")
    del draw


def noise():
    image = open_image_file()
    image_data = get_image_data(image)
    draw = ImageDraw.Draw(image)
    factor = 100
    for i in range(image_data.width):
        for j in range(image_data.height):
            rand = random.randint(-factor, factor)
            a = image_data.pixels[i, j][0] + rand
            b = image_data.pixels[i, j][1] + rand
            c = image_data.pixels[i, j][2] + rand
            if a < 0:
                a = 0
            if b < 0:
                b = 0
            if c < 0:
                c = 0
            if a > 255:
                a = 255
            if b > 255:
                b = 255
            if c > 255:
                c = 255
            draw.point((i, j), (a, b, c))
    image.save("src/result_noise.jpg", "JPEG")
    del draw


def brightness(factor):
    image = open_image_file()
    image_data = get_image_data(image)
    draw = ImageDraw.Draw(image)
    for i in range(image_data.width):
        for j in range(image_data.height):
            a = image_data.pixels[i, j][0] + factor
            b = image_data.pixels[i, j][1] + factor
            c = image_data.pixels[i, j][2] + factor
            if a < 0:
                a = 0
            if b < 0:
                b = 0
            if c < 0:
                c = 0
            if a > 255:
                a = 255
            if b > 255:
                b = 255
            if c > 255:
                c = 255
            draw.point((i, j), (a, b, c))
    image.save("src/result_brightness.jpg", "JPEG")
    del draw
