import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QLabel, QScrollArea, QWidget, QMainWindow, QSizePolicy,
                             QHBoxLayout, QVBoxLayout, QBoxLayout,
                             QSlider, QPushButton, QSpacerItem, QIcon)
from PyQt5.QtGui import QImage, QPixmap, QShowEvent
from PyQt5.QtCore import Qt, pyqtSignal


class CenterWidget(QWidget):
    def __init__(self, widget_to_center: QWidget, layout: QBoxLayout):
        super().__init__()
        layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        layout.addWidget(widget_to_center)
        layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.setLayout(layout)


class ImageWindow(QMainWindow):
    def __init__(self, image=None, parent=None):
        super().__init__(parent)
        self.scroll_area = QScrollArea()
        self.image_label = QLabel()
        self.image = image or QImage("")

        self.image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.image_label.setVisible(False)
        self.image_label.setScaledContents(True)
        self.scroll_area.setWidget(CenterWidget(self.image_label, layout=QHBoxLayout()))
        self.scroll_area.setWidgetResizable(True)
        self.setCentralWidget(self.scroll_area)

    def refresh(self, image):
        self.image = image or QImage("")
        aspect_ratio_mode = Qt.AspectRatioMode.KeepAspectRatio
        transformation_mode = Qt.TransformationMode.SmoothTransformation
        pixmap = QPixmap.fromImage(self.image)
        pixmap = pixmap.scaled(self.parent().size(), aspect_ratio_mode, transformation_mode)
        self.image_label.setPixmap(pixmap)
        self.image_label.setVisible(True)


class Slider(QWidget):
    value_changed = pyqtSignal(int)
    def __init__(self, name:str, min_val: int, max_val: int):
        super().__init__()

        self._slider = QSlider(Qt.Orientation.Horizontal)
        self._slider.setMinimum(min_val)
        self._slider.setMaximum(max_val)
        self._slider.setTickInterval(1)
        self._slider.setStyleSheet("""
            QSlider {
                background-color: #2c3e50;
            }

            QSlider::groove:horizontal {
                background-color: #bdc3c7;
                height: 4px;
                border-radius: 2px;
            }

            QSlider::handle:horizontal {
                background-color: #ecf0f1;
                border: none;
                height: 12px;
                width: 12px;
                margin: -5px 0;
                border-radius: 6px;
            }
        """)

        value_label = QLabel(str(self._slider.value()))
        value_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        h_layout = QHBoxLayout()
        h_layout.addWidget(QLabel(name))
        h_layout.addWidget(value_label)

        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self._slider)
        self.setLayout(v_layout)

        self._slider.valueChanged.connect(lambda value: value_label.setText(str(value)))
        self._slider.valueChanged.connect(lambda value: self.value_changed.emit(value))

    def showEvent(self, a0: QShowEvent) -> None:
        self._slider.setValue(0)
        return super().showEvent(a0)


class EditWindow(QWidget):
    onAccept = pyqtSignal()
    onCancel = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setVisible(False)

    def createUI(self, layout: QBoxLayout):
        v_layout = QVBoxLayout()
        v_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        v_layout.addLayout(layout)

        h_layout = QHBoxLayout()
        cancel_button = QPushButton("Cancel")
        apply_button = QPushButton("Apply")
        h_layout.addWidget(cancel_button)
        h_layout.addWidget(apply_button)
        v_layout.addLayout(h_layout)

        cancel_button.clicked.connect(self.hide)
        cancel_button.clicked.connect(self.onCancel.emit)
        apply_button.clicked.connect(self.onAccept.emit)
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #ecf0f1;
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-size: 16px;
            }

            QPushButton:hover {
                background-color: #95a5a6;
            }

            QPushButton:pressed {
                background-color: transparent;
                border: 1px solid #ecf0f1;
            }
        """)
        apply_button.setStyleSheet("""
            QPushButton {
                background-color: #bdc3c7;
                color: #2c3e50;
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-size: 16px;
            }

            QPushButton:hover {
                background-color: #d0d3d4;
            }

            QPushButton:pressed {
                background-color: #bdc3c7;
                border: 1px solid #2c3e50;
            }
        """)
        self.setLayout(v_layout)

