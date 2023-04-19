from __future__ import annotations

import cv2
import numpy as np
import matplotlib.pyplot as plt


class Image:
    def __init__(self, data: np.ndarray) -> None:
        self.data = data.copy()

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

    def get_histogram(self, channel: int) -> np.ndarray:
        return np.histogram(self.data[:, :, channel], bins=256, range=(0, 256))[0]

    def create_histogram_figure(self) -> plt.figure:
        figure = plt.figure()
        ax = figure.add_subplot(111)
        if self.num_channels == 3:
            colors = ("red", "green", "blue")
            for idx, color in enumerate(colors):
                ax.plot(self.get_histogram(idx), color=color)
        else:
            ax.plot(self.get_histogram(0), color="black")
        ax.set_title("Histogram")
        return figure

    def set_brightness(self, brightness: int) -> None:
        if brightness > 0:
            array = np.full(self.data.shape, brightness, dtype=np.uint8)
            cv2.add(self.data, array, self.data)
        else:
            array = np.full(self.data.shape, -brightness, dtype=np.uint8)
            cv2.subtract(self.data, array, self.data)

    def set_contrast(self, contrast: int) -> None:
        data = self.data.astype(np.int16)
        if contrast >= 0:
            factor = (259 * (contrast + 255)) / (255 * (259 - contrast))
        else:
            factor = (259 * (contrast + 255)) / (255 * (259 + contrast))
        self.data = np.clip((factor * (data - 128) + 128), 0, 255).astype(np.uint8)

    @staticmethod
    def _run_for_valid_kernel_size(func):
        def wrapper(self, size: int, *args) -> None:
            size = size if size % 2 == 1 and size > 1 else max(3, size + 1)
            func(self, size, *args)
        return wrapper

    @_run_for_valid_kernel_size
    def average_filter(self, size: int) -> None:
        cv2.blur(self.data, (size, size), self.data)

    @_run_for_valid_kernel_size
    def gaussian_blur(self, size: int) -> None:
        sigma = size / 6
        cv2.GaussianBlur(self.data, (size, size), sigma, self.data, sigma)

    @_run_for_valid_kernel_size
    def median_filter(self, size: int) -> None:
        cv2.medianBlur(self.data, size, self.data)
