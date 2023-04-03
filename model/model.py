from model.processing import Image

import numpy as np
import matplotlib.pyplot as plt
from typing import Union


class Model:
    def __init__(self):
        self.image = None

    def open_image(self, image_path: str):
        self.image = Image.open(image_path)

    def get_image(self) -> Union[np.ndarray, None]:
        return self.image.data if self.image else None

    def save_image(self, image_path: str):
        self.image.save(image_path)

    def set_image(self, image: Union[np.ndarray, None]):
        self.image = image

    def get_histogram_figure(self) -> Union[plt.figure, None]:
        return self.image.create_histogram_figure()