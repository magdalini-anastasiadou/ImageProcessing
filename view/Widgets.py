from PyQt5.QtWidgets import (QLabel, QScrollArea, QWidget, QMainWindow, QSizePolicy,
                             QHBoxLayout, QVBoxLayout, QBoxLayout,
                             QSlider, QPushButton, QSpacerItem)
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

        name_label = QLabel(name)
        self._value_label = QLabel(str(self._slider.value()))
        self._value_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        h_layout = QHBoxLayout()
        h_layout.addWidget(name_label)
        h_layout.addWidget(self._value_label)

        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self._slider)
        self.setLayout(v_layout)

        self._slider.valueChanged.connect(lambda value: self._value_label.setText(str(value)))
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

        with open('view/cancel_button.qss') as f:
            stylesheet = f.read()
            cancel_button.setStyleSheet(stylesheet)
        
        with open('view/apply_button.qss') as f:
            stylesheet = f.read()
            apply_button.setStyleSheet(stylesheet)

        self.setLayout(v_layout)