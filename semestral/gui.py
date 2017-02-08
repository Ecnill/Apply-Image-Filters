import os
import shutil

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDesktopWidget

from image_operations import color_invert, gray_scale, send_image_from_gui, brightness, sepia, noise, \
     blur, sharpen, get_image_size, TempFile


TEMP_FILE_PATH = TempFile()


class ImageViewer(QtWidgets.QLabel):
    def __init__(self, path, tmp_path):
        super().__init__()
        self.path = path
        self.tmp_path = tmp_path
        pix_map = QPixmap(path)
        self.setPixmap(pix_map)
        self.scale_factor = 2.0

    def update(self, path=''):
        pix_map = QPixmap(path)
        self.setPixmap(pix_map)

    def scale_image(self, factor):
        self.scale_factor *= factor
        w = self.scale_factor * self.width()
        h = self.scale_factor * self.height()
        if self.tmp_path != '':
            path = self.tmp_path
        else:
            path = self.path
        pix_max = QPixmap(path)
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
        self.last_dir = os.path.curdir + '/examples'
        self.tmp_path = ''
        self.scroll_area = self.win.findChild(QtWidgets.QScrollArea, 'scrollArea')
        self.init_ui()

    def init_ui(self):
        self.center()
        self._update_title()
        self._action('actionOpen').triggered.connect(self._open)
        self._action('actionSave').triggered.connect(self._save)
        self._action('actionSave_as').triggered.connect(self._save_as)
        self._action('actionInvert').triggered.connect(self.do_color_invert)
        self._action('actionGrayScale').triggered.connect(self.do_gray_scale)
        self._action('actionSepia').triggered.connect(self.do_sepia)
        self._action('actionBrightnessMore').triggered.connect(self.do_brightness_more)
        self._action('actionBrightnessLess').triggered.connect(self.do_brightness_less)
        self._action('actionZoomIn').triggered.connect(self.zoom_in)
        self._action('actionZoomOut').triggered.connect(self.zoom_out)
        self._action('actionNoise').triggered.connect(self.do_noise)
        self._action('actionQuit').triggered.connect(self._close)
        self._action('actionImage_Properties').triggered.connect(self.image_properties)
        self._action('actionBlur').triggered.connect(self.do_blur)
        self._action('actionSharpen').triggered.connect(self.do_sharpen)

    def set_menu_items_enabled(self):
        self._action('actionInvert').setEnabled(True)
        self._action('actionBlur').setEnabled(True)
        self._action('actionSharpen').setEnabled(True)
        self._action('actionSave_as').setEnabled(True)
        self._action('actionGrayScale').setEnabled(True)
        self._action('actionBlackWhite').setEnabled(True)
        self._action('actionSepia').setEnabled(True)
        self._action('actionNoise').setEnabled(True)
        self._action('actionBrightnessMore').setEnabled(True)
        self._action('actionBrightnessLess').setEnabled(True)
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
        send_image_from_gui(path, TEMP_FILE_PATH.temp_path)  # connection with image_operations
        self.tmp_path = TEMP_FILE_PATH.temp_path
        self.label = ImageViewer(path, self.tmp_path)
        self.label.scale_factor = 1.0
        self.scroll_area.setWidget(self.label)
        self.filename = os.path.basename(path)
        self._update_title()
        self.set_menu_items_enabled()

    def _save_as(self, path):
        if not path:
            path = self.last_dir
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self.win, 'Save image', path, 'Image files (*.jpg *.png)')
        if not path:
            return
        path += os.path.splitext(self.tmp_path)[1]
        self.last_dir = os.path.dirname(path)
        shutil.copyfile(self.tmp_path, path)

    def _save(self):
        path = os.path.join(self.home_dir, self.filename)
        shutil.copyfile(self.tmp_path, path)
        self._action('actionSave').setEnabled(False)
        self._update_title()

    def image_properties(self):
        w, h = get_image_size()
        full_path = os.path.join(self.home_dir, self.filename)
        info = 'Size in pixels: %d x %d \n\nNumber of pixels: %d\n\nFilepath: %s\n\nFile size: %s' \
               % (w, h, w * h, full_path, self.convert_file_size(os.path.getsize(self.tmp_path)))
        QtWidgets.QMessageBox.information(self.win, self.filename, info, QtWidgets.QMessageBox.Ok)

    def image_action(self, operation, *args):
        self._action('actionZoomIn').setEnabled(True)
        self._action('actionZoomOut').setEnabled(True)
        operation(*args)
        self.label.update(self.tmp_path)
        self._update_title('*')
        self._action('actionSave').setEnabled(True)

    def do_color_invert(self):
        self.image_action(color_invert)

    def do_gray_scale(self):
        self.image_action(gray_scale)

    def do_sepia(self):
        self.image_action(sepia)

    def do_noise(self):
        self.image_action(noise)

    def do_blur(self):
        self.image_action(blur)

    def do_sharpen(self):
        self.image_action(sharpen)

    def do_brightness_more(self):
        self.do_brightness(50)

    def do_brightness_less(self):
        self.do_brightness(-50)

    def do_brightness(self, brightness_level):
        self.image_action(brightness, brightness_level)

    def zoom_in(self):
        self.zoom(1.25)

    def zoom_out(self):
        self.zoom(0.8)

    def zoom(self, factor):
        self.label.scale_image(factor)
        self.adjust_scroll_bar(self.scroll_area.horizontalScrollBar(), factor)
        self.adjust_scroll_bar(self.scroll_area.verticalScrollBar(), factor)
        self._action('actionSave').setEnabled(True)

    @staticmethod
    def convert_file_size(size_in_bytes):
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        if size_in_bytes == 0:
            return '0 B'
        i = 0
        while size_in_bytes >= 1024 and i < len(suffixes) - 1:
            size_in_bytes /= 1024.
            i += 1
        f = ('%.2f' % size_in_bytes).rstrip('0').rstrip('.')
        return '%s %s' % (f, suffixes[i])

    @staticmethod
    def adjust_scroll_bar(scroll_bar, factor):
        scroll_bar.setValue(int(factor * scroll_bar.value() + ((factor - 1) * scroll_bar.pageStep() / 2)))


def main():
    try:
        TEMP_FILE_PATH.create_temp_file()
        gui = Gui()
        return gui.run()
    finally:
        TEMP_FILE_PATH.close_temp_file()
