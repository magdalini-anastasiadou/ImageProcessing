from model.processing import Image
from model.signal import Signal

import numpy as np
import matplotlib.pyplot as plt
from typing import Union


class Model:
    image_changed = Signal()

    def __init__(self):
        self.image = None

    def open_image(self, image_path: str):
        self.image = Image.open(image_path)
        self.image_changed.emit()

    def get_image(self) -> Union[np.ndarray, None]:
        return self.image.data if self.image else None

    def save_image(self, image_path: str):
        self.image.save(image_path)

    def set_image(self, image: Union[np.ndarray, None]):
        self.image = image
        self.image_changed.emit()

    def get_histogram_figure(self) -> Union[plt.figure, None]:
        return self.image.create_histogram_figure() if self.image else None