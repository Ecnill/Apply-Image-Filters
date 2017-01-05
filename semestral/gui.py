import os

from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDesktopWidget

from image_operations import color_invert, gray_scale, black_white, noise, sepia, brightness, set_image_path


class ImageViewer(QtWidgets.QLabel):
    def __init__(self, pixmap):
        super().__init__()
        self.pixmap = pixmap
        self.setPixmap(pixmap)


class Gui(object):
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.win = QtWidgets.QMainWindow()

        with open('ui/mainwindow.ui') as f:
            uic.loadUi(f, self.win)

        self.filename = '-'
        self.last_dir = os.path.curdir
        self.init_ui()
        self.scroll_area = self.win.findChild(QtWidgets.QScrollArea, 'scrollArea')
        self._action('actionOpen').triggered.connect(self._open)

    def init_ui(self):
        self.center()
        icon = QtGui.QIcon('src/tau.png')
        self.win.setWindowIcon(icon)
        self._update_title()

    def set_menu_items_enabled(self):
        self._action('actionInvert').setEnabled(True)
        self._action('actionInvert').triggered.connect(self.do_color_invert)
        self._action('actionGrayscale').setEnabled(True)
        self._action('actionGrayscale').triggered.connect(self.do_gray_scale)
        self._action('actionBlackWhite').setEnabled(True)
        self._action('actionBlackWhite').triggered.connect(self.do_black_white)
        self._action('actionSepia').setEnabled(True)
        self._action('actionSepia').triggered.connect(self.do_sepia)
        self._action('actionNoise').setEnabled(True)
        self._action('actionNoise').triggered.connect(self.do_noise)
        self._action('actionBrightnessMore').setEnabled(True)
        self._action('actionBrightnessMore').triggered.connect(self.do_brightness_more)
        self._action('actionBrightnessLess').setEnabled(True)
        self._action('actionBrightnessLess').triggered.connect(self.do_brightness_less)

    def _action(self, name):
        return self.win.findChild(QtWidgets.QAction, name)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.win.geometry()
        self.win.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

    def _update_title(self, changed=''):
        self.win.setWindowTitle('Graphics editor [{}]'.format(self.filename + ' ' + changed))

    def run(self):
        self.win.show()
        return self.app.exec_()

    def _open(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self.win,'Open File', self.last_dir + '/src')
        if not path:
            return
        self.last_dir = os.path.dirname(path)
        p = QPixmap(path)
        label = ImageViewer(p)
        self.scroll_area.setWidget(label)
        self.filename = os.path.basename(path)
        self._update_title()
        self.set_menu_items_enabled()
        set_image_path(path)

    def do_color_invert(self):
        color_invert()
        p = QPixmap('src/result_invert.jpg')
        label = ImageViewer(p)
        self.scroll_area.setWidget(label)
        self._update_title('*')

    def do_gray_scale(self):
        gray_scale()
        p = QPixmap('src/result_gray.jpg')
        label = ImageViewer(p)
        self.scroll_area.setWidget(label)
        self._update_title('*')

    def do_black_white(self):
        black_white()
        p = QPixmap('src/result_bw.jpg')
        label = ImageViewer(p)
        self.scroll_area.setWidget(label)
        self._update_title('*')

    def do_sepia(self):
        sepia()
        p = QPixmap('src/result_sepia.jpg')
        label = ImageViewer(p)
        self.scroll_area.setWidget(label)
        self._update_title('*')

    def do_noise(self):
        noise()
        p = QPixmap('src/result_noise.jpg')
        label = ImageViewer(p)
        self.scroll_area.setWidget(label)
        self._update_title('*')

    def do_brightness_more(self):
        brightness(100)
        p = QPixmap('src/result_brightness.jpg')
        label = ImageViewer(p)
        self.scroll_area.setWidget(label)
        self._update_title('*')

    def do_brightness_less(self):
        brightness(-100)
        p = QPixmap('src/result_brightness.jpg')
        label = ImageViewer(p)
        self.scroll_area.setWidget(label)
        self._update_title('*')


def main():
    gui = Gui()
    return gui.run()


