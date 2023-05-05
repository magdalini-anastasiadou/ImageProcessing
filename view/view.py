from view.Widgets import ImageWindow, Slider, EditWindow

import numpy as np
from PyQt5.QtWidgets import (QMainWindow, QApplication, QStackedWidget, QFileDialog, QSpacerItem,
                             QVBoxLayout, QPushButton, QHBoxLayout, QWidget, QSizePolicy, QAction)
from PyQt5.QtGui import QImage, QIcon
from PyQt5.QtCore import Qt


class ImageEditor(QMainWindow):
    def initUI(self, presenter):
        self.presenter = presenter
        self.create_central_widget()
        self.create_actions()
        self.setWindowTitle("Image Editor")
        self.setWindowIcon(QIcon("view/icons/design.png"))
        self.set_window_style()
        self.showMaximized()

    def create_actions(self):
        open_action = QAction(self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        self.addAction(open_action)

        save_action = QAction(self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        self.addAction(save_action)

        exit_action = QAction(self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)

    def create_central_widget(self):
        self.side_bar = self.create_sidebar()
        self.side_bar.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.image_label = ImageWindow(self)
        self.image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        widget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.side_bar)
        layout.addWidget(self.image_label)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        widget.setLayout(layout)
        layout.setStretchFactor(self.side_bar, 1)
        layout.setStretchFactor(self.image_label, 30)
        self.setCentralWidget(widget)

    def create_sidebar(self):
        menu_btn = QPushButton(QIcon("view/icons/menu.png"), "")
        menu_btn.setFlat(True)

        open_btn = QPushButton(QIcon("view/icons/add-image.png", ), "")
        open_btn.setFlat(True)
        open_btn.clicked.connect(self.open_file)

        light_window = self.create_light_window()
        edit_btn = QPushButton(QIcon("view/icons/edit.png"), "")
        edit_btn.setFlat(True)
        edit_btn.clicked.connect(lambda: light_window.setVisible(not light_window.isVisible()))

        save_btn = QPushButton(QIcon("view/icons/download.png", ), "")
        save_btn.setFlat(True)
        save_btn.clicked.connect(self.save_file)

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(20)
        sidebar_layout.setContentsMargins(0, 20, 0, 0)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        sidebar_layout.addWidget(open_btn)
        sidebar_layout.addWidget(edit_btn)
        sidebar_layout.addWidget(save_btn)

        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0, 0, 0, 0)
        hboxLayout.setSpacing(0)
        hboxLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        hboxLayout.addLayout(sidebar_layout)
        hboxLayout.addWidget(light_window)

        sidebar_widget = QWidget()
        sidebar_widget.setLayout(hboxLayout)
        
        stacked_widget1 = QStackedWidget()
        stacked_widget1.addWidget(QWidget())
        stacked_widget1.addWidget(sidebar_widget)
        stacked_widget1.setCurrentIndex(1)

        menu_btn.clicked.connect(lambda: stacked_widget1.setCurrentIndex(stacked_widget1.currentIndex() == 0))

        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(menu_btn)
        vboxLayout.addWidget(stacked_widget1)
        vboxLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        vboxLayout.setContentsMargins(10, 20, 0, 0)

        widget = QWidget()
        widget.setLayout(vboxLayout)
        widget.setStyleSheet("background-color: #2c3e50;")
        return widget

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

    def open_file(self):
        dialog = QFileDialog()
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        dialog.setNameFilter("Images (*.png *.jpg)")
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
        window = EditWindow()
        window.onCancel.connect(self.presenter.handle_cancel)
        window.onAccept.connect(self.presenter.handle_accept)

        b_slider = Slider("Brightness", -100, 100)
        c_slider = Slider("Contrast", -100, 100)
        g_slider = Slider("Blur", 0, 10)

        b_slider.value_changed.connect(self.presenter.handle_brightness_changed)
        c_slider.value_changed.connect(self.presenter.handle_contrast_changed)
        g_slider.value_changed.connect(self.presenter.handle_gaussian_blur)

        layout = QVBoxLayout()
        layout.addWidget(b_slider)
        layout.addWidget(c_slider)
        layout.addWidget(g_slider)
        window.createUI(layout)
        return window