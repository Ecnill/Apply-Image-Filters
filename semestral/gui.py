import os
import shutil

from PyQt5 import QtGui, QtWidgets, uic, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDesktopWidget

from image_operations import color_invert, gray_scale, black_white, set_image_data, brightness, sepia, noise, \
    TempFiles, get_image_size

temp_files = TempFiles(4)
IMAGE_TMP_PATHS = []


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


class Window(QtWidgets.QMainWindow):
    def get_close_dialog_answer(self):
        result = QtWidgets.QMessageBox.question(self, 'Confirm Exit...', 'Your image is not saved, '
                                                                         'are you sure you want to exit?',
                                                QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        return result == QtWidgets.QMessageBox.Yes

    def closeEvent(self, event):
        if '*' in self.windowTitle():
            result = self.get_close_dialog_answer()
            if result:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


class Gui(object):
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.win = Window()

        with open('ui/mainwindow.ui') as f:
            uic.loadUi(f, self.win)
        self.filename = '-'
        self.home_dir = ''
        self.last_dir = os.path.curdir + '/src'
        self.current_path = ''
        self.scroll_area = self.win.findChild(QtWidgets.QScrollArea, 'scrollArea')
        self.init_ui()

    def init_ui(self):
        self.center()
        icon = QtGui.QIcon('src/tau.png')
        self.win.setWindowIcon(icon)
        self._update_title()
        self._action('actionOpen').triggered.connect(self._open)
        self._action('actionSave').triggered.connect(self._save)
        self._action('actionSave_as').triggered.connect(self._save_as)
        self._action('actionInvert').triggered.connect(self.do_color_invert)
        self._action('actionGrayScale').triggered.connect(self.do_gray_scale)
        self._action('actionBlackWhite').triggered.connect(self.do_black_white)
        self._action('actionSepia').triggered.connect(self.do_sepia)
        self._action('actionBrightnessMore').triggered.connect(self.do_brightness_more)
        self._action('actionBrightnessLess').triggered.connect(self.do_brightness_less)
        self._action('actionZoomIn').triggered.connect(self.zoom_in)
        self._action('actionZoomOut').triggered.connect(self.zoom_out)
        self._action('actionNoise').triggered.connect(self.do_noise)
        self._action('actionQuit').triggered.connect(self._close)
        self._action('actionImage_Properties').triggered.connect(self.image_properties)

    def set_menu_items_enabled(self):
        self._action('actionInvert').setEnabled(True)
        self._action('actionSave_as').setEnabled(True)
        self._action('actionGrayScale').setEnabled(True)
        self._action('actionBlackWhite').setEnabled(True)
        self._action('actionSepia').setEnabled(True)
        self._action('actionNoise').setEnabled(True)
        self._action('actionBrightnessMore').setEnabled(True)
        self._action('actionBrightnessLess').setEnabled(True)
        self._action('actionZoomIn').setEnabled(True)
        self._action('actionZoomOut').setEnabled(True)
        self._action('actionImage_Properties').setEnabled(True)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.win.geometry()
        self.win.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def run(self):
        self.win.show()
        return self.app.exec_()

    def _update_title(self, changed=''):
        self.title = 'Graphics editor - {}'.format(self.filename + ' ' + changed)
        self.win.setWindowTitle(self.title)

    def _action(self, name):
        return self.win.findChild(QtWidgets.QAction, name)

    def _close(self):
        if '*' in self.title:
            result = self.win.get_close_dialog_answer()
            if result:
                self.win.close()
        else:
            self.win.close()

    def _open(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self.win, 'Open File', self.last_dir)
        if not path:
            return
        self.last_dir = os.path.dirname(path)
        self.home_dir = self.last_dir
        self.current_path = path
        self.label = ImageViewer(path)
        self.scroll_area.setWidget(self.label)
        self.filename = os.path.basename(path)
        self._update_title()
        self.set_menu_items_enabled()
        self.label.scale_factor = 1.0
        set_image_data(path)  # connection with image_operations

    def _save_as(self, path):
        if not path:
            path = self.last_dir
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self.win, 'Save image', path, 'Image files (*.jpg *.png)')
        if not path:
            return
        path += os.path.splitext(self.current_path)[1]
        self.last_dir = os.path.dirname(path)
        shutil.copyfile(self.current_path, path)

    def _save(self):
        path = os.path.join(self.home_dir, self.filename)
        shutil.copyfile(self.current_path, path)
        self._action('actionSave').setEnabled(False)
        self._update_title()

    def image_properties(self):
        w, h = get_image_size()
        full_path = os.path.join(self.home_dir, self.filename)
        info = 'Size in pixels: %d x %d \n\nNumber of pixels: %d\n\nFilepath: %s\n\nFile size: %d' \
               % (w, h, w * h, full_path, os.path.getsize(self.current_path))  # todo: convert file size to mb
        QtWidgets.QMessageBox.information(self.win, self.filename, info, QtWidgets.QMessageBox.Ok)

    def do_color_invert(self):
        new_path = color_invert()
        self.label.update(new_path)
        self._update_title('*')
        self.current_path = new_path
        self._action('actionSave').setEnabled(True)

    def do_gray_scale(self):
        new_path = gray_scale()
        self.label.update(new_path)
        self._update_title('*')
        self.current_path = new_path
        self._action('actionSave').setEnabled(True)

    def do_black_white(self):
        new_path = black_white()
        self.label.update(new_path)
        self._update_title('*')
        self.current_path = new_path
        self._action('actionSave').setEnabled(True)

    def do_sepia(self):
        new_path = sepia()
        self.label.update(new_path)
        self._update_title('*')
        self.current_path = new_path
        self._action('actionSave').setEnabled(True)

    def do_noise(self):
        new_path = noise()
        self.label.update(new_path)
        self._update_title('*')
        self.current_path = new_path
        self._action('actionSave').setEnabled(True)

    def do_brightness_more(self):
        self.do_brightness(100)

    def do_brightness_less(self):
        self.do_brightness(-100)

    def do_brightness(self, brightness_level):
        new_path = brightness(brightness_level)
        self.label.update(new_path)
        self._update_title('*')
        self.current_path = new_path
        self._action('actionSave').setEnabled(True)

    def zoom_in(self):
        self.zoom(1.25)

    def zoom_out(self):
        self.zoom(0.7)

    def zoom(self, factor):
        self.label.scale_image(factor, self.current_path)
        self.adjust_scroll_bar(self.scroll_area.horizontalScrollBar(), factor)
        self.adjust_scroll_bar(self.scroll_area.verticalScrollBar(), factor)
        self._action('actionSave').setEnabled(True)

    @staticmethod
    def adjust_scroll_bar(scroll_bar, factor):
        scroll_bar.setValue(int(factor * scroll_bar.value() + ((factor - 1) * scroll_bar.pageStep() / 2)))


def main():
    try:
        global IMAGE_TMP_PATHS
        IMAGE_TMP_PATHS = temp_files.get_tmp_files()
        gui = Gui()
        return gui.run()
    finally:
        temp_files.remove_tmp_dir()
