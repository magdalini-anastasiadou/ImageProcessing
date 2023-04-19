from view.Widgets import ImageArea, PlotWindow, Slider, EditWindow, SpinBox

import numpy as np
from PyQt5.QtWidgets import (QMainWindow, QApplication, QAction, QFileDialog,
                             QVBoxLayout, QGridLayout, QLabel)
from PyQt5.QtGui import QImage, QIcon


class ImageEditor(QMainWindow):
    def initUI(self, presenter):
        self.presenter = presenter
        self.plot_window = PlotWindow(self)
        self.create_central_widget()

        self.setWindowTitle("Image Editor")
        self.setWindowIcon(QIcon("view/icons/colour.png"))
        self.create_file_menu()
        self.create_edit_menu()
        self.create_adjust_menu()
        self.create_view_menu()
        self.set_window_style()
        self.showMaximized()

    def create_central_widget(self):
        self.image_label = ImageArea(self)
        self.light_window = self.create_light_window()
        self.filters_window = self.create_filters_window()

        self.setCentralWidget(self.image_label)

    def create_file_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")

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

    def create_edit_menu(self):
        menuBar = self.menuBar()
        edit_menu = menuBar.addMenu("&Edit")

        undo_action = QAction("&Undo", self)
        undo_action.setShortcut('Ctrl+Z')
        undo_action.triggered.connect(self.presenter.handle_undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction("&Redo", self)
        redo_action.setShortcut('Ctrl+Y')
        redo_action.triggered.connect(self.presenter.handle_redo)
        edit_menu.addAction(redo_action)


    def create_adjust_menu(self):
        menu_bar = self.menuBar()
        adjust_menu = menu_bar.addMenu("&Adjust")

        light_action = QAction('&Light', self)
        light_action.triggered.connect(self.light_window.show)
        adjust_menu.addAction(light_action)

        filters_action = QAction('&Blur', self)
        filters_action.triggered.connect(self.filters_window.show)
        adjust_menu.addAction(filters_action)

    def create_view_menu(self):
        menu_bar = self.menuBar()
        view_menu = menu_bar.addMenu("&View")

        histogram_action = QAction('&Histogram', self)
        histogram_action.triggered.connect(self.presenter.handle_show_histogram)
        view_menu.addAction(histogram_action)

    def set_window_style(self):
        with open('view/stylesheet.qss') as f:
            app = QApplication.instance()
            stylesheet = f.read()
            app.setStyleSheet(stylesheet)

    def set_data(self, data: np.ndarray):
        if data is not None:
            h, w = data.shape[:2]
            image = QImage(data, w, h, 3 * w, QImage.Format.Format_RGB888)
            self.image_label.refresh(image)
        else:
            self.setWindowTitle("Image Editor")
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
            self.presenter.handle_open_file(path)

    def save_file(self):
        dialog = QFileDialog()
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        window_title = self.windowTitle()
        dialog.selectFile(window_title)
        dialog.setNameFilter("Images (*.png *.xpm *.jpg *.bmp *.gif)")
        if dialog.exec():
            path = dialog.selectedFiles()[0]
            self.presenter.handle_save_file(path)

    def create_light_window(self):
        b_slider = Slider("Brightness", 'view/icons/sun.png', -100, 100)
        b_slider.value_changed.connect(self.presenter.handle_brightness_changed)
        c_slider = Slider("Contrast", 'view/icons/contrast.png', -100, 100)
        c_slider.value_changed.connect(self.presenter.handle_contrast_changed)
        window = EditWindow("Light", "view/icons/sunny-black.png")
        window.onCancel.connect(self.presenter.handle_cancel)
        window.onAccept.connect(self.presenter.handle_accept)
        layout = QVBoxLayout()
        layout.addWidget(b_slider)
        layout.addWidget(c_slider)
        window.createUI(layout)
        return window

    def create_filters_window(self):
        window = EditWindow("Filters", "view/icons/magic-wand.png")
        layout = QGridLayout()
        s1 = SpinBox(0, 10)
        s2 = SpinBox(0, 10)
        s3 = SpinBox(0, 10)
        layout.addWidget(QLabel("Average Blur"), 0, 0)
        layout.addWidget(s1, 0, 1)
        layout.addWidget(QLabel("Fuzzy Blur"), 1, 0)
        layout.addWidget(s2, 1, 1)
        layout.addWidget(QLabel("Median Blur"), 2, 0)
        layout.addWidget(s3, 2, 1)
        s1.value_changed.connect(self.presenter.handle_average_filter)
        s2.value_changed.connect(self.presenter.handle_gaussian_blur)
        s3.value_changed.connect(self.presenter.handle_median_blur)
        window.createUI(layout)
        window.onCancel.connect(self.presenter.handle_cancel)
        window.onAccept.connect(self.presenter.handle_accept)
        return window