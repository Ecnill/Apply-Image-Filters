#!/usr/bin/env python3
# coding: utf-8
# author: Ecnill
# created: 15.10.2016

""" Zahrejte si na molekulu:
Vystartujte z náhodného místa konzole
náhodným směrem a na okrajích konzole se odrážejte
podle (ideálního) zákona odrazu. """

import os
import time
import random
import sys


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def draw_border(length, height):
    print('\033[34m' + "#" * length, end='')
    for i in range(1, height - 2):
        print('#', '{:^{spaces}}'.format("", spaces=length - 2), '#', sep='')
    print("#" * length + '\033[0m', end='')


def print_char_here(x, y, char):
    x = int(x)
    y = int(y)
    horiz = str(x)
    vert = str(y)
    print("\033[" + vert + ";" + horiz + "f" + "\033[" + str(random.randint(31, 37)) + "m", char, "\033[0m")


def erase_chars(pos_x, pos_y):
    print_char_here(pos_x, pos_y, ' ')


def draw_square(pos_x, pos_y):
    print_char_here(pos_x, pos_y, '\u25A0')


def move(screen_size, pos, direction):
    erase_chars(pos[0], pos[1])
    pos[0] += direction[0]
    pos[1] += direction[1]
    draw_square(pos[0], pos[1])
    if pos[0] == 2 or pos[0] == screen_size[0]:
        direction[0] *= -1
    if pos[1] == 3 or pos[1] == screen_size[1]:
        direction[1] *= -1
    return [pos, direction]


def render_loop(speed=0.3):
    ts = os.get_terminal_size()
    clear_screen()
    os.system('setterm -cursor off')
    columns = ts.columns
    lines = ts.lines - 1
    print('\033[31m' + 'BI-PYT hometask #01:' + '\033[34m' + ' Molekula.' + '\033[0m')
    draw_border(columns, lines)
    height = lines - 1
    length = columns - 3
    screen_size = [length, height]
    vector = [random.choice((-1, 1)), random.choice((-1, 1))]
    square_pos = [random.randint(2, length), random.randint(3, height)]  # x, y
    while True:
        square_pos, vector = move(screen_size, square_pos, vector)
        time.sleep(speed)


if __name__ == "__main__":
    try:
        arg_len = len(sys.argv)
        if arg_len > 1:
            render_loop(float(sys.argv[1]))
        else:
            render_loop()
    except KeyboardInterrupt:
        clear_screen()
        os.system('setterm -cursor on')
