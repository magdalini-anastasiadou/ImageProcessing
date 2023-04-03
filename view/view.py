from view.Widgets import ImageArea, PlotWindow

import numpy as np
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QFileDialog
from PyQt5.QtGui import QIcon, QImage
from typing import Protocol


class Presenter(Protocol):
    def handle_new_image(self):
        pass

    def handle_open_image(self, image_path: str):
        pass

    def handle_save_image(self, image_path: str):
        pass

    def handle_show_histogram(self):
        pass


class ImageEditor(QMainWindow):
    def initUI(self, presenter: Presenter):
        self.presenter = presenter
        self.image_label = ImageArea(self)
        self.plot_window = PlotWindow(self)
        self.setCentralWidget(self.image_label)

        self.setWindowTitle("Image Editor")
        self.setWindowIcon(QIcon("view/icons/colour.png"))
        self.create_file_menu()
        self.create_edit_menu()
        self.create_adjust_menu()
        self.create_view_menu()
        self.set_window_style()
        self.showMaximized()

    def create_file_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')

        new_file_action = QAction('New File', self)
        new_file_action.setShortcut('Ctrl+N')
        new_file_action.triggered.connect(self.presenter.handle_new_image)
        file_menu.addAction(new_file_action)

        open_file_action = QAction('Open File...', self)
        open_file_action.setShortcut('Ctrl+O')
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        save_file_action = QAction('Save', self)
        save_file_action.setShortcut('Ctrl+S')
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def create_edit_menu(self):
        menu_bar = self.menuBar()
        edit_menu = menu_bar.addMenu('Edit')

        undo_action = QAction('Undo', self)
        undo_action.setShortcut('Ctrl+Z')
        undo_action.setEnabled(False)
        edit_menu.addAction(undo_action)

        redo_action = QAction('Redo', self)
        redo_action.setShortcut('Ctrl+Y')
        redo_action.setEnabled(False)
        edit_menu.addAction(redo_action)
    
    def create_adjust_menu(self):
        menu_bar = self.menuBar()
        adjust_menu = menu_bar.addMenu('Adjust')

        gray_scale_action = QAction(QIcon('view/icons/grayscale.png'), '&Auto B&&W', self)
        adjust_menu.addAction(gray_scale_action)

        brightness_action = QAction(QIcon('view/icons/sunny.png'), '&Brightness', self)
        adjust_menu.addAction(brightness_action)

    def create_view_menu(self):
        menu_bar = self.menuBar()
        view_menu = menu_bar.addMenu('View')

        histogram_action = QAction(QIcon('view/icons/histogram.png'), '&Histogram', self)
        histogram_action.triggered.connect(self.presenter.handle_show_histogram)
        view_menu.addAction(histogram_action)

    def set_window_style(self):
        with open('view/stylesheet.qss') as f:
            app = QApplication.instance()
            stylesheet = f.read()
            app.setStyleSheet(stylesheet)

    def set_image(self, data: np.ndarray):
        if data is not None:
            h, w = data.shape[:2]
            image = QImage(data, w, h, 3 * w, QImage.Format.Format_RGB888)
            self.image_label.refresh(image)
        else:
            self.image_label.refresh(None)

    def set_plot(self, figure):
        if figure is not None:
            self.plot_window.refresh(figure)
        else:
            self.plot_window.setVisible(False)

    def is_plot_visible(self):
        return self.plot_window.isVisible()

    def open_file(self):
        dialog = QFileDialog()
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        dialog.setNameFilter("Images (*.png *.xpm *.jpg *.bmp *.gif)")
        if dialog.exec():
            path = dialog.selectedFiles()[0]
            self.setWindowTitle(path)
            self.presenter.handle_open_image(path)

    def save_file(self):
        dialog = QFileDialog()
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        window_title = self.windowTitle()
        dialog.selectFile(window_title)
        dialog.setNameFilter("Images (*.png *.xpm *.jpg *.bmp *.gif)")
        if dialog.exec():
            path = dialog.selectedFiles()[0]
            self.presenter.handle_save_image(path)