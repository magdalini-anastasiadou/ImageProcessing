from model.processing import Image
from model.signal import Signal

import numpy as np
import matplotlib.pyplot as plt
from typing import Union, Any



class Model():
    image_changed = Signal()

    def __init__(self):
        self.image = None
        self._methods_map = {
            "brightness": Image.set_brightness, 
            "contrast": Image.set_contrast, 
            "average_filter": Image.average_filter,
            "gaussian_blur": Image.gaussian_blur,
        }
        self._edit_actions = []
        self._last_accepted_idx = 0

    def open_file(self, image_path: str):
        self._edit_actions.clear()
        self.image = Image.open(image_path)
        self.image_changed.emit()

    def save_file(self, image_path: str):
        if self.image:
            self.image.save(image_path)

    def clear(self):
        self.image = None
        self.image_changed.emit()

    def _get_image_with_edits(self) -> Union[Image, None]:
        img = self.image
        for method, value, use_last in self._edit_actions:
            if use_last:
                img = Image(img.data)
                method(img, value)
            else:
                method(value)
        return img

    def get_data(self) -> Union[np.ndarray, None]:
        return self._get_image_with_edits().data if self.image else None

    def get_histogram_figure(self) -> Union[plt.figure, None]:
        image = self._get_image_with_edits()
        return image.create_histogram_figure() if self.image else None

    def set_attribute(self, name: str, value: Any):
        if name in self._methods_map:
            action = (self._methods_map[name], value, True)
            if self._edit_actions and self._edit_actions[-1][0] == self._methods_map[name]:
                self._edit_actions[-1] = action
            else:
                self._edit_actions.append(action)
            self.image_changed.emit()

    def accept(self):
        self._edit_actions.append((lambda v: True, None, False))
        self._last_accepted_idx = len(self._edit_actions)

    def cancel(self):
        self._edit_actions = self._edit_actions[:self._last_accepted_idx]
        self.image_changed.emit()