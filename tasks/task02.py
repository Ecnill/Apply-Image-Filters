#!/usr/bin/env python3
# coding:   utf-8
# author:   Ecnill
# title:    Ulam spiral
# created:  22.10.16

import os
from math import sqrt, floor


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def is_prime(a):
    if a < 2:
        return False
    for i in range(2, int(sqrt(a)) + 1):
        if a % i == 0:
            return False
    return True


def set_numb_view(numb):
    view = '\033[47m' if is_prime(numb) else '\033[0m'
    return view + '{:{prec}d}'.format(numb, prec=4)


def spiral_item(n, x, y):
    d, y, x = 0, y - n//2, x - (n - 1)//2
    l = 2 * max(abs(x), abs(y))
    d = (l*3 + x + y) if y >= x else (l - x - y)
    return (l - 1)**2 + d


def show_spiral():
    n = floor(os.get_terminal_size().columns / 5)
    for y in range(n):
        for x in range(n):
            print(set_numb_view(spiral_item(n, x, y)), end=' ')
        print()

if __name__ == '__main__':
    clear_screen()
    print('\033[31m' + 'BI-PYT hometask #02:' + '\033[34m' + ' Ulam spiral.' + '\033[0m')
    show_spiral()


