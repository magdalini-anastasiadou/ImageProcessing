from __future__ import annotations

import cv2
import numpy as np


class Image:
    def __init__(self, data: np.ndarray) -> None:
        self.data = data

    @property
    def num_channels(self):
        return self.data.shape[2]

    @classmethod
    def open(cls, image_path: str) -> Image:
        data = cv2.imread(image_path)
        image = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
        return cls(image)

    def save(self, image_path: str) -> None:
        image = cv2.cvtColor(self.data, cv2.COLOR_RGB2BGR)
        cv2.imwrite(image_path, image)