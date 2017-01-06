import os

from PyQt5 import QtGui, QtWidgets, uic, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import Qt

from image_operations import color_invert, gray_scale, black_white, noise, sepia, brightness, set_image_path, tmp_images


IMAGE_TMP_PATHS = []


def delete_tmp_files():
    for path in IMAGE_TMP_PATHS:
        if os.path.exists(path):
            os.remove(path)


class ImageViewer(QtWidgets.QLabel):
    def __init__(self, path):
        super().__init__()
        self.path = path
        pix_map = QPixmap(path)
        self.setPixmap(pix_map)
        self.scale_factor = 2.0

    def update(self, path=''):
        pix_map = QPixmap(path)
        self.setPixmap(pix_map)

    def scale_image(self, factor, current_path=''):
        if current_path == '':
            current_path = self.path
        self.scale_factor *= factor
        w = self.scale_factor * self.width()
        h = self.scale_factor * self.height()
        pix_max = QPixmap(current_path)
        self.setPixmap(pix_max.scaled(w, h, QtCore.Qt.KeepAspectRatio))


class Gui(object):
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.win = QtWidgets.QMainWindow()
        with open('ui/mainwindow.ui') as f:
            uic.loadUi(f, self.win)

        self.filename = '-'
        self.last_dir = os.path.curdir
        self.current_path = ''
        self.init_ui()
        self.scroll_area = self.win.findChild(QtWidgets.QScrollArea, 'scrollArea')
        self._action('actionOpen').triggered.connect(self._open)
        self._action('actionQuit').triggered.connect(self._close)

    def init_ui(self):
        self.center()
        icon = QtGui.QIcon('src/tau.png')
        self.win.setWindowIcon(icon)
        self._update_title()

    def set_menu_items_enabled(self):
        self._action('actionInvert').setEnabled(True)
        self._action('actionInvert').triggered.connect(self.do_color_invert)
        self._action('actionGrayScale').setEnabled(True)
        self._action('actionGrayScale').triggered.connect(self.do_gray_scale)
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
        self._action('actionZoomIn').setEnabled(True)
        self._action('actionZoomIn').triggered.connect(self.zoom_in)
        self._action('actionZoomOut').setEnabled(True)
        self._action('actionZoomOut').triggered.connect(self.zoom_out)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.win.geometry()
        self.win.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

    def run(self):
        self.win.show()
        return self.app.exec_()

    def _update_title(self, changed=''):
        self.win.setWindowTitle('Graphics editor - {}'.format(self.filename + ' ' + changed))

    def _action(self, name):
        return self.win.findChild(QtWidgets.QAction, name)

    def _open(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self.win,'Open File', self.last_dir + '/src')
        if not path:
            return
        self.last_dir = os.path.dirname(path)
        self.current_path = path
        self.label = ImageViewer(path)
        self.scroll_area.setWidget(self.label)
        self.filename = os.path.basename(path)
        self._update_title()
        self.set_menu_items_enabled()
        self.label.scale_factor = 1.0
        set_image_path(path)            # connection with image_operations

    def _close(self):
        delete_tmp_files()
        self.win.close()

    def do_color_invert(self):
        new_path = color_invert()
        self.label.update(new_path)
        self._update_title('*')
        self.current_path = new_path

    def do_gray_scale(self):
        new_path = gray_scale()
        self.label.update(new_path)
        self._update_title('*')
        self.current_path = new_path

    def do_black_white(self):
        new_path = black_white()
        self.label.update(new_path)
        self._update_title('*')
        self.current_path = new_path

    def do_sepia(self):
        new_path = sepia()
        self.label.update(new_path)
        self._update_title('*')
        self.current_path = new_path

    def do_noise(self):
        new_path = noise()
        self.label.update(new_path)
        self._update_title('*')
        self.current_path = new_path

    def do_brightness_more(self):
        new_path = brightness(100)
        self.label.update(new_path)
        self._update_title('*')
        self.current_path = new_path

    def do_brightness_less(self):
        new_path = brightness(-100)
        self.label.update(new_path)
        self._update_title('*')
        self.current_path = new_path

    def zoom_in(self):
        self.zoom(1.25)

    def zoom_out(self):
        self.zoom(0.8)

    def zoom(self, factor):
        self.label.scale_image(factor, self.current_path)
        self.adjust_scroll_bar(self.scroll_area.horizontalScrollBar(), factor)
        self.adjust_scroll_bar(self.scroll_area.verticalScrollBar(), factor)

    @staticmethod
    def adjust_scroll_bar(scroll_bar, factor):
        scroll_bar.setValue(int(factor * scroll_bar.value() + ((factor - 1) * scroll_bar.pageStep() / 2)))


def main():
    global IMAGE_TMP_PATHS
    IMAGE_TMP_PATHS = tmp_images()
    gui = Gui()
    return gui.run()
