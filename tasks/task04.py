#!/usr/bin/env python3
# coding:   utf-8
# author:   Ecnill
# title:    Mandelbrot set
# created:  26.12.16

import sys
from math import log

from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor

Width = 600
Height = 600


class MandelbrotGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.m = MandelbrotCalculation()
        self.init_ui()

    def init_ui(self):

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
        self.resize(Width, Width)
        self.center()
        self.setWindowTitle('Mandelbrot set')
        self.statusBar().setStyleSheet("QStatusBar{padding-left:8px;background:black;color:white;font-weight:bold;}")
        self.statusBar().showMessage('Press +, -, UP, DOWN, LEFT, RIGHT. Keep calm, it runs slowly.')
        self.show()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            QApplication.quit()
        elif key == Qt.Key_Plus:
            self.m.crop /= 2.5
            print('+')
        elif key == Qt.Key_Minus:
            self.m.crop *= 2.5
            print('-')
        elif key == Qt.Key_Right:
            self.m.offset_x += self.m.crop / 1.5
            print('RIGHT')
        elif key == Qt.Key_Left:
            self.m.offset_x -= self.m.crop / 1.5
            print('LEFT')
        elif key == Qt.Key_Down:
            self.m.offset_y -= self.m.crop / 1.5
            print('DOWN')
        elif key == Qt.Key_Up:
            self.m.offset_y += self.m.crop / 1.5
            print('UP')
        self.update()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.m.mandel()
        self.draw_points(self.m.coords, self.m.colors, qp)
        qp.end()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

    @staticmethod
    def draw_points(coords, colors, qp):
        for i in range(len(coords)):
            qp.setPen(QColor(colors[i][0], colors[i][1], colors[i][2]))
            x = coords[i][0]
            y = coords[i][1]
            qp.drawPoint(x, y)


class MandelbrotCalculation:
    coords = []
    colors = []
    depth = 100
    crop = 3.0
    width = Width
    height = Height
    offset_x, offset_y = 0, 0

    def mandel(self):
        print('Computing Mandelbrot set...')
        self.coords.clear()
        self.colors.clear()
        de = int(self.depth)
        for x in range(0, self.width):
            real = x / (self.width / self.crop) - self.crop / 2 + self.offset_x
            for y in range(0, self.height):
                img = y / (self.height / self.crop) - self.crop / 2 + self.offset_y
                c = complex(real, img)
                z = 0
                i = 0
                while i < de:
                    z = z * z + c
                    if abs(z) >= 2:
                        break
                    i += 1
                # set colors by some absurd magic
                if i != self.depth:
                    r = (i - log(log(abs(z)))) / log(2) * 10
                    r = int(r) % 255
                    g = (i - log(log(abs(z)))) / log(2) * 5
                    g = int(g) % 255
                    b = (i - log(log(abs(z)))) / log(13) * 42
                    b = int(b) % 255
                    self.colors.append((r, g, b))
                    self.coords.append((x, y))


if __name__ == '__main__':
    app = QApplication([])
    run = MandelbrotGUI()
    sys.exit(app.exec_())
