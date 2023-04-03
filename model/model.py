from model.processing import Image

import numpy as np


class Model:
    def __init__(self):
        self.image = None

    def open_image(self, image_path: str):
        self.image = Image.open(image_path)

    def get_image(self) -> np.ndarray:
        return self.image.data if self.image else None

    def save_image(self, image_path: str):
        self.image.save(image_path)

    def set_image(self, image: np.ndarray):
        self.image = image