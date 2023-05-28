from view.Widgets import ImageWindow, Slider, EditWindow, UndoValueCommand, UndoRedoCommand

import numpy as np
from PyQt5.QtWidgets import (QMainWindow, QApplication, QStackedWidget, QFileDialog, QUndoStack, QSpinBox,
                             QVBoxLayout, QPushButton, QHBoxLayout, QWidget, QSizePolicy, QAction, QLabel)
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

        self.undo_stack = QUndoStack(self)
        undo_action = QAction("Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.undo_stack.undo)
        self.addAction(undo_action)
        
        redo_action = QAction("Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self.undo_stack.redo)
        self.addAction(redo_action)

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
        open_btn.clicked.connect(lambda: self.undo_stack.clear())

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
        vboxLayout.setContentsMargins(20, 20, 20, 0)

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
        def undo_accept():
            self.presenter.handle_cancel_accept()
            window.show()
        
        def redo_accept():
            self.presenter.handle_accept()
            window.hide()

        window.onAccept.connect(
            lambda: self.undo_stack.push(
                UndoRedoCommand(window, redo_accept, undo_accept)
            )  if not window.isUndoRedoActive() else None
        )
        rotation_row = QHBoxLayout()
        rotation_row.setContentsMargins(0, 20, 0, 20)
        rotate_left_btn = QPushButton(QIcon("view/icons/rotate-left.png"), "")
        rotate_left_btn.setToolTip("Rotate left")
        rotate_right_btn = QPushButton(QIcon("view/icons/rotate-right.png"), "")
        rotate_right_btn.setToolTip("Rotate right")
        flip_horizontally_btn = QPushButton(QIcon("view/icons/flip-horizontally.png"), "")
        flip_horizontally_btn.setToolTip("Flip horizontally")
        flip_vertically_btn = QPushButton(QIcon("view/icons/flip-vertically.png"), "")
        flip_vertically_btn.setToolTip("Flip vertically")

        rotate_left_btn.clicked.connect(
            lambda: self.undo_stack.push(
                UndoRedoCommand(rotate_left_btn, self.presenter.handle_rotate_left, self.presenter.handle_rotate_right)
            )
        )
        rotate_right_btn.clicked.connect(
            lambda: self.undo_stack.push(
                UndoRedoCommand(rotate_right_btn, self.presenter.handle_rotate_right, self.presenter.handle_rotate_left)
            )
        )
        flip_horizontally_btn.clicked.connect(
            lambda: self.undo_stack.push(
                UndoRedoCommand(flip_horizontally_btn, self.presenter.handle_flip_horizontally, self.presenter.handle_flip_horizontally)
            )
        )
        flip_vertically_btn.clicked.connect(
            lambda: self.undo_stack.push(
                UndoRedoCommand(flip_vertically_btn, self.presenter.handle_flip_vertically, self.presenter.handle_flip_vertically)
            )
        )

        rotate_left_btn.setFlat(True)
        rotate_right_btn.setFlat(True)
        flip_horizontally_btn.setFlat(True)
        flip_vertically_btn.setFlat(True)

        rotation_row.addWidget(rotate_left_btn)
        rotation_row.addWidget(rotate_right_btn)
        rotation_row.addWidget(flip_horizontally_btn)
        rotation_row.addWidget(flip_vertically_btn)

        def create_slider(name, min_value, max_value):
            widget = QWidget()

            slider = Slider(Qt.Orientation.Horizontal)
            slider.setRange(min_value, max_value)
            slider.setValue(0)
            value_label = QLabel("0")
            value_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            slider.valueChanged.connect(lambda value: value_label.setText(str(value)))
            name_label = QLabel(name)

            def on_accept():
                if not window.isUndoRedoActive():
                    slider.blockSignals(True)
                    slider.setValue(0)
                    slider.blockSignals(False)
                    value_label.setText("0")

            def on_cancel():
                if not window.isUndoRedoActive():
                    slider.blockSignals(True)
                    slider.setValue(0)
                    slider.blockSignals(False)
                    value_label.setText("0")

            window.onAccept.connect(on_accept)
            window.onCancel.connect(on_cancel)

            hlayout = QHBoxLayout()
            hlayout.addWidget(name_label)
            hlayout.addWidget(value_label)
            hlayout.setContentsMargins(0, 0, 0, 0)
            hlayout.setSpacing(0)

            vlayout = QVBoxLayout()
            vlayout.addLayout(hlayout)
            vlayout.addWidget(slider)
            vlayout.setContentsMargins(0, 0, 0, 0)
            widget.setLayout(vlayout)

            return widget, slider
    
        b_slider_widget, b_slider = create_slider("Brightness", -100, 100)
        c_slider_widget, c_slider = create_slider("Contrast", -100, 100)
        g_slider_widget, g_slider = create_slider("Blur", 0, 10)
        s_slider_widget, s_slider = create_slider("Sharpen", 0, 10)

        b_slider.valueChanged.connect(
            lambda value: self.undo_stack.push(
                UndoValueCommand(b_slider, self.presenter.handle_brightness_changed, value, b_slider.previous_value())
            ) if not b_slider.isUndoRedoActive() else None
        )
        c_slider.valueChanged.connect(
            lambda value: self.undo_stack.push(
                UndoValueCommand(c_slider, self.presenter.handle_contrast_changed, value, c_slider.previous_value())
            ) if not c_slider.isUndoRedoActive() else None
        )
        g_slider.valueChanged.connect(
            lambda value: self.undo_stack.push(
                UndoValueCommand(g_slider, self.presenter.handle_gaussian_blur, value, g_slider.previous_value())
            ) if not g_slider.isUndoRedoActive() else None
        )
        s_slider.valueChanged.connect(
            lambda value: self.undo_stack.push(
                UndoValueCommand(s_slider, self.presenter.handle_sharpen, value, s_slider.previous_value())
            ) if not s_slider.isUndoRedoActive() else None
        )

        layout = QVBoxLayout()
        layout.addWidget(b_slider_widget)
        layout.addWidget(c_slider_widget)
        layout.addWidget(g_slider_widget)
        layout.addWidget(s_slider_widget)
        layout.addLayout(rotation_row)
        window.createUI(layout)
        return window