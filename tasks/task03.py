#!/usr/bin/env python3
# coding:   utf-8
# author:   Ecnill
# title:    Brownian motion
# created:  05.11.16

import os
import time
import sys
import numpy as np
from collections import namedtuple
from random import choice, randint

Screen_Size = namedtuple('Screen_Size', ['length', 'height'])
Coordinate = namedtuple('Coordinate', ['x', 'y'])

move_direction = [Coordinate(-1, -1), Coordinate(0, -1), Coordinate(1, -1), Coordinate(-1, 0), Coordinate(1, 0),
                  Coordinate(-1, 1), Coordinate(0, 1), Coordinate(1, 1)]

background_color = [255, 255, 255]
molecule_color = [0, 0, 150]


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_molecule_here(direction, color=[0, 0, 0]):
    print('\x1b[48;2;%s;%s;%sm\033[%s;%sf' % (color[0], color[1], color[2], direction[1], direction[0])
          + ' ' + '\033[0m')


def set_background_color(screen_size, color):
    print('\033[1;0f')
    for i in range(0, screen_size.height):
        for j in range(0, screen_size.length):
            print('\x1b[48;2;%s;%s;%sm' % (color[0], color[1], color[2]) + ' ' + '\033[0m', end='')
        print()


def print_title():
    print('\033[0;0f\x1b[38;2;%s;%s;%sm' % (255, 0, 0)
          + 'BI-PYT hometask #03. ' + '\x1b[38;2;%s;%s;%sm' % (255, 0, 255) + 'Brownian motion' + '\033[0m')


def render_loop(screen_size, speed=0.1):
    while True:
        print_title()
        set_background_color(screen_size, background_color)
        pos = np.array([screen_size.length // 2, screen_size.height // 2])
        screen_matrix = [[background_color for x in range(0, screen_size.height + 2)]
                         for y in range(0, screen_size.length + 1)]

        while pos[0] != screen_size.length and pos[1] != screen_size.height + 2 and pos[0] != 0 and pos[1] != 1:
            step = randint(1, 5)
            curr_dir = choice(move_direction)
            while step != 0:
                if screen_matrix[pos[0]][pos[1]] == molecule_color:
                    r, g, b = randint(0, 254), randint(0, 254), randint(0, 254)
                    if r == 0 and g == 0 and b == 150:
                        continue
                    screen_matrix[pos[0]][pos[1]] = curr_color = [r, g, b]
                    print_molecule_here(pos, curr_color)
                else:
                    curr_color = molecule_color
                print_molecule_here(pos, curr_color)
                screen_matrix[pos[0]][pos[1]] = molecule_color
                pos += curr_dir
                step -= 1
                if pos[0] == screen_size.length or pos[1] == screen_size.height + 2 or pos[0] == 0 or pos[1] == 1:
                    break
                time.sleep(speed)
        time.sleep(0.5)
        clear_screen()


if __name__ == '__main__':
    clear_screen()
    os.system('setterm -cursor off')

    length = os.get_terminal_size().columns
    height = os.get_terminal_size().lines - 2
    screen_size = Screen_Size(length, height)

    try:
        arg_len = len(sys.argv)
        if arg_len > 1:
            render_loop(screen_size, float(sys.argv[1]))
        else:
            render_loop(screen_size)
    except KeyboardInterrupt:
        clear_screen()
        os.system('setterm -cursor on')
