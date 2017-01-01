#!/usr/bin/env python3
# coding:   utf-8
# author:   Ecnill
# title:    PNG to PNM converter
# created:  27.12.16

import struct
import sys
import zlib
import os.path
from collections import namedtuple

FILENAME = 'input.png'

PNG_HEADER_LENGTH = 8
PNG_HEADER = 0x89504E470D0A1A0A
LENGTH_CHUNK_DATA = 4
LENGTH_CHUNK_TYPE = 4
LENGTH_CHUNK_CRC = 4
LENGTH_IHDR_CHUNK = 13

ImageHeader = namedtuple('ImageHeader', [
    'width', 'height', 'depth', 'color_type', 'compression', 'filter', 'interlace'])


class WrongHeaderSizeError(Exception):
    def __init__(self):
        self.message = 'Wrong header of PNG file!'


class WrongIHDRSizeError(Exception):
    def __init__(self):
        self.message = 'Wrong size of IHDR chunk!'


class WrongCRCSizeError(Exception):
    def __init__(self, chunk_type):
        self.message = 'Wrong CRC size of %s chunk! ' % chunk_type


def is_png_header_correct(header):
    head, = struct.unpack('>Q', bytes(header))
    return head == PNG_HEADER


def read_ihdr_chunk_data(data):
    return ImageHeader(*struct.unpack_from('>IIBBBBB', data))


def get_pixels(data, w):
    array = bytearray(data)
    pixels = []
    i = 1
    while i <= len(array) - 3:
        if i % (w * 3 + 1) == 0:
            i += 1
        pixels += [(array[i], array[i + 1], array[i + 2])]
        i += 3
    return pixels


def rgb_to_str(pixel):
    return '%d %d %d ' % pixel


def do_convert(height, width, data):
    with open('result.ppm', 'w') as f:
        f.write('P3\n')
        f.write('%d %d\n' % (width, height))
        f.write('255\n')
        img = ''
        for i in range(len(data)):
            img += rgb_to_str(data[i])
            if (i + 1) % width == 0:
                img += '\n'
        f.write(img)


def read_png(filename):
    with open(filename, 'rb') as f:
        header = None

        data = f.read(PNG_HEADER_LENGTH)
        if not is_png_header_correct(data):
            raise WrongHeaderSizeError

        while True:
            data = f.read(LENGTH_CHUNK_DATA)
            if not data:
                break

            chunk_length, = struct.unpack_from('>I', data)
            chunk_type = f.read(LENGTH_CHUNK_TYPE).decode()

            if chunk_type == 'IEND':
                crc, = struct.unpack('>I', f.read(LENGTH_CHUNK_CRC))
                if crc != zlib.crc32(chunk_type.encode()):
                    raise WrongCRCSizeError(chunk_type)
                break

            else:
                data = f.read(chunk_length)
                crc, = struct.unpack('>I', f.read(LENGTH_CHUNK_CRC))

                if crc != zlib.crc32(chunk_type.encode() + data):
                    raise WrongCRCSizeError(chunk_type)

                if chunk_type == 'IHDR':
                    if chunk_length != LENGTH_IHDR_CHUNK:
                        raise WrongIHDRSizeError
                    header = read_ihdr_chunk_data(data)

                elif chunk_type == 'IDAT':
                    yield header.width, header.height, data

                else:
                    print('Unknown or unchecked data type: ' + chunk_type)


def convert_png_to_pnm(filename):
    extension = os.path.splitext(filename)[1]
    base_filename = os.path.basename(filename)
    if not os.path.exists(filename) or extension.lower() != '.png':
        raise FileNotFoundError(base_filename)

    ww, hh = -1, -1
    data = b''
    print('Start converting file %s from PNG to PPM format...' % base_filename)
    try:
        for width, height, chunk in read_png(filename):
            ww, hh = width, height
            data += chunk
        decompressed_data = zlib.decompress(data)
        do_convert(hh, ww, get_pixels(decompressed_data, ww))
    except WrongHeaderSizeError as e:
        print(e.message)
    except WrongIHDRSizeError as e:
        print(e.message)
    except WrongCRCSizeError as e:
        print(e.message)
    finally:
        print('Done')


if __name__ == '__main__':
    arg_len = len(sys.argv)
    try:
        if arg_len > 1:
            convert_png_to_pnm(str(sys.argv[1]))
        else:
            convert_png_to_pnm(FILENAME)
    except FileNotFoundError as e:
        print('No such file %s or file extension is not PNG!' % e.args)
