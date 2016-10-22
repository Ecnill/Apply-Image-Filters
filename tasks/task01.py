#!/usr/bin/env python3
# coding:   utf-8
# author:   Ecnill
# title:    Molecule
# created:  15.10.2016

""" Zahrejte si na molekulu:
Vystartujte z náhodného místa konzole
náhodným směrem a na okrajích konzole se odrážejte
podle (ideálního) zákona odrazu. """

import os
import time
import sys
from random import randint, choice
from collections import namedtuple


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def draw_border(length, height):
    print('\033[34m' + '#' * length, end='')
    for i in range(1, height - 2):
        print('#', '{:^{spaces}}'.format('', spaces=length - 2), '#', sep='')
    print('#' * length + '\033[0m', end='')


def print_char_here(x, y, char):
    print('\033[%s;%sf\033[%sm' % (int(y), int(x), randint(31, 37)), char, '\033[0m')


def erase_chars(pos_x, pos_y):
    print_char_here(pos_x, pos_y, ' ')


def draw_square(pos_x, pos_y):
    print_char_here(pos_x, pos_y, '\u25A0')


def move(screen_size, pos, direction):
    erase_chars(pos[0], pos[1])
    pos[0] += direction[0]
    pos[1] += direction[1]
    draw_square(pos[0], pos[1])
    if pos[0] == 2 or pos[0] == screen_size.length:
        direction[0] *= -1
    if pos[1] == 3 or pos[1] == screen_size.height:
        direction[1] *= -1
    return [pos, direction]


def render_loop(speed=0.1):
    ts = os.get_terminal_size()
    columns = ts.columns
    lines = ts.lines - 1
    print('\033[31m' + 'BI-PYT hometask #01:' + '\033[34m' + ' Molekule.' + '\033[0m')
    draw_border(columns, lines)
    height = lines - 1
    length = columns - 3
    Screen_Size = namedtuple('Screen_Size', ['length', 'height'])
    vector = [choice((-1, 1)), choice((-1, 1))]
    square_pos = [randint(2, length), randint(3, height)]     # x, y
    while True:
        square_pos, vector = move(Screen_Size(length, height), square_pos, vector)
        time.sleep(speed)


if __name__ == '__main__':
    clear_screen()
    os.system('setterm -cursor off')
    try:
        arg_len = len(sys.argv)
        if arg_len > 1:
            render_loop(float(sys.argv[1]))
        else:
            render_loop()
    except KeyboardInterrupt:
        clear_screen()
        os.system('setterm -cursor on')
