import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QLabel, QSizePolicy, QScrollArea, QWidget, 
                             QHBoxLayout, QVBoxLayout, QBoxLayout, QDockWidget, 
                             QSlider, QPushButton, QSpinBox)
from PyQt5.QtGui import QImage, QPixmap, QShowEvent, QIcon
from PyQt5.QtCore import Qt, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class Spacer(QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)


class CenterWidget(QWidget):
    def __init__(self, widget_to_center: QWidget, layout: QBoxLayout):
        super().__init__()
        left_spacer = Spacer()
        right_spacer = Spacer()
        layout.addWidget(left_spacer)
        layout.addWidget(widget_to_center)
        layout.addWidget(right_spacer)
        self.setLayout(layout)


class ImageArea(QScrollArea):
    def __init__(self, image=None, parent=None):
        super().__init__(parent)
        self.image_label = QLabel(self)
        self.image = image or QImage("")
        self.image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.image_label.setVisible(False)

        self.setWidget(CenterWidget(self.image_label, layout=QHBoxLayout()))
        self.setWidgetResizable(True)

    def refresh(self, image):
        self.image = image or QImage("")
        pixmap = QPixmap.fromImage(self.image)
        aspect_ratio_mode = Qt.AspectRatioMode.KeepAspectRatio
        transformation_mode = Qt.TransformationMode.SmoothTransformation
        pixmap = pixmap.scaled(self.parent().size(), aspect_ratio_mode, transformation_mode)
        self.image_label.setPixmap(pixmap)
        self.image_label.setVisible(True)


class PlotWindow(QDockWidget):
    def __init__(self, parent=None):
        super().__init__("Plot", parent)
        self.setVisible(False)
        self.setFeatures(self.features() | QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.setFloating(True)
        self.setWidget(self.canvas)

    def refresh(self, figure):
        self.canvas.figure = figure
        self.canvas.draw()
        self.adjustSize()
        self.setVisible(True)


class SpinBox(QSpinBox):
    value_changed = pyqtSignal(int)
    def __init__(self, min_val: int, max_val: int, step: int = 1):
        super().__init__()
        self.setMinimum(min_val)
        self.setMaximum(max_val)
        self.setSingleStep(step)
        self.editingFinished.connect(lambda: self.value_changed.emit(self.value()))


    def showEvent(self, a0: QShowEvent) -> None:
        self.setValue(0)
        return super().showEvent(a0)


class Slider(QWidget):
    value_changed = pyqtSignal(int)
    def __init__(self, name:str, icon:str, min_val: int, max_val: int):
        super().__init__()

        self._slider = QSlider(Qt.Orientation.Horizontal)
        self._slider.setMinimum(min_val)
        self._slider.setMaximum(max_val)
        self._slider.setTickInterval(1)

        icon = QPixmap(icon)
        icon_label = QLabel()
        icon_label.setPixmap(icon)
        name_label = QLabel(name)
        self._value_label = QLabel(str(self._slider.value()))
        self._value_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        h_layout = QHBoxLayout()
        h_layout.addWidget(icon_label)
        h_layout.addWidget(name_label)
        h_layout.addWidget(Spacer())
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


class EditWindow(QDockWidget):
    onAccept = pyqtSignal()
    onCancel = pyqtSignal()

    def __init__(self, title: str, icon_path: str, parent=None):
        super().__init__(title, parent)
        self.setFloating(True)
        self.setFeatures(self.features() | QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(icon_path))
        self.setVisible(False)

    def createUI(self, layout: QBoxLayout):
        v_layout = QVBoxLayout()
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

        temp = QWidget()
        temp.setLayout(v_layout)
        self.setWidget(temp)