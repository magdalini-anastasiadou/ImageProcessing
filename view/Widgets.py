from PyQt5.QtWidgets import QLabel, QSizePolicy, QScrollArea, QWidget, QHBoxLayout, QBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt


class CenterWidget(QWidget):
    def __init__(self, widget_to_center: QWidget, layout: QBoxLayout):
        super().__init__()
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

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
