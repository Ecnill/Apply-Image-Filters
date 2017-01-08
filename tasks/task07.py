#!/usr/bin/env python3
# coding:   utf-8
# author:   Ecnill
# title:    Sharpen filters
# created:  08.01.17

import os
import sys
import mimetypes
from PIL import Image, ImageDraw
from collections import namedtuple

FILENAME = 'kvetina.jpg'

ImageData = namedtuple('ImageData', ['width', 'height', 'pixels'])

SharpenFilter = namedtuple('SharpenFilter', ['name', 'filter'])

sharpen_one = SharpenFilter('sharpen_one', [
    [1, 1, 1],
    [1, -7, 1],
    [1, 1, 1]
])

sharpen_two = SharpenFilter('sharpen_two', [
    [-1, -1, -1],
    [-1, 9, -1],
    [-1, -1, -1]
])

sharpen_three = SharpenFilter('sharpen_three', [
    [-1, -1, -1, -1, -1],
    [-1, 2, 2, 2, -1],
    [-1, 2, 8, 2, -1],
    [-1, 2, 2, 2, -1],
    [-1, -1, -1, -1, -1]
])


def sharpen(filename, filter_sharpen, result_name, factor=1.0, bias=0.0):
    base_filename = os.path.basename(filename)
    if 'image' not in mimetypes.guess_type(FILENAME)[0] or not os.path.exists(filename):
        raise FileNotFoundError(base_filename)

    image = Image.open(filename)
    im = ImageData(image.size[0], image.size[1], image.load())
    new_image = Image.new('RGB', [im.width, im.height], (255, 255, 255))
    draw = ImageDraw.Draw(new_image)

    print('Applying %s filter to file %s...' % (filter_sharpen.name, base_filename))

    for x in range(im.width):
        for y in range(im.height):
            r, g, b = 0.0, 0.0, 0.0

            for fy in range(len(filter_sharpen.filter)):
                for fx in range(len(filter_sharpen.filter[0])):

                    im_x = (x - len(filter_sharpen.filter[0]) / 2 + fx + im.width) % im.width
                    im_y = (y - len(filter_sharpen.filter) / 2 + fy + im.height) % im.height

                    r += im.pixels[im_x, im_y][0] * filter_sharpen.filter[fy][fx]
                    g += im.pixels[im_x, im_y][1] * filter_sharpen.filter[fy][fx]
                    b += im.pixels[im_x, im_y][2] * filter_sharpen.filter[fy][fx]

            r = min(max(int(factor * r + bias), 0), 255)
            g = min(max(int(factor * g + bias), 0), 255)
            b = min(max(int(factor * b + bias), 0), 255)
            draw.point((x, y), (r, g, b))

    new_image.save(result_name, 'JPEG')
    print('Done. Please check out file %s.\n' % os.path.abspath(result_name))
    del draw


if __name__ == '__main__':
    arg_len = len(sys.argv)
    if arg_len > 1:
        file = str(sys.argv[1])
    else:
        file = FILENAME
    try:
        sharpen(file, sharpen_one, 'result_1.jpg')
        sharpen(file, sharpen_two, 'result_2.jpg')
        sharpen(file, sharpen_three, 'result_3.jpg', 1.0 / 8.5)
    except FileNotFoundError as e:
        print('No such file %s or file is not image!' % e.args)
