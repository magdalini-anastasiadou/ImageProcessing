from model.processing import Image
from model.signal import Signal

import numpy as np
import matplotlib.pyplot as plt
from typing import Union


class Model:
    image_changed = Signal()

    def __init__(self):
        self.image = None
        self.current_idx = 0
        self.actions = []

    def open_image(self, image_path: str):
        self.image = Image.open(image_path)
        self.image_changed.emit()

    def get_image(self) -> Union[np.ndarray, None]:
        if self.image:
            data = self.image.data
            for action, args in self.actions:
                image = Image(data)
                action(image, *args)
                data = image.data
            return data

    def save_image(self, image_path: str):
        self.image.save(image_path)

    def set_image(self, image: Union[np.ndarray, None]):
        self.image = image
        self.image_changed.emit()

    def get_histogram_figure(self) -> Union[plt.figure, None]:
        return self.image.create_histogram_figure() if self.image else None

    def set_brightness(self, brightness: int):
        if self.current_idx == len(self.actions):
            self.actions.append((Image.set_brightness, (brightness, )))
        else:
            self.actions[self.current_idx] = (Image.set_brightness, (brightness, ))
        self.image_changed.emit()
    
    def set_contrast(self, contrast: int):
        if self.current_idx == len(self.actions):
            self.actions.append((Image.set_contrast, (contrast, )))
        else:
            self.actions[self.current_idx] = (Image.set_contrast, (contrast, ))
        self.image_changed.emit()

    def accept(self):
        self.current_idx += 1

    def cancel(self):
        self.actions = self.actions[:len(self.actions) - 1]
        self.current_idx = len(self.actions)
        self.image_changed.emit()