from __future__ import annotations

import cv2
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


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
        data = self.data.astype(np.int16)
        self.data = np.clip(data + brightness, 0, 255).astype(np.uint8)

    def set_contrast(self, contrast: int) -> None:
        data = self.data.astype(np.int16)
        if contrast >= 0:
            factor = (259 * (contrast + 255)) / (255 * (259 - contrast))
        else:
            factor = (259 * (contrast + 255)) / (255 * (259 + contrast))
        self.data = np.clip((factor * (data - 128) + 128), 0, 255).astype(np.uint8)

    def _convolve(self, kernel: np.ndarray) -> None:
        red = signal.convolve(self.data[:, :, 0], kernel, mode="same")
        green = signal.convolve(self.data[:, :, 1], kernel, mode="same")
        blue = signal.convolve(self.data[:, :, 2], kernel, mode="same")
        self.data = np.dstack((red, green, blue))
        self.data = np.clip(self.data, 0, 255).astype(np.uint8)

    def average_filter(self, size: int) -> None:
        if size != 0:
            kernel = np.ones((size, size)) / (size * size)
            self._convolve(kernel)

    def gaussian_blur(self, size: int) -> None:
        if size != 0:
            if size % 2 == 0:
                size += 1
            sigma = size / 6
            x, y = np.meshgrid(
                np.linspace(-1, 1, size),
                np.linspace(-1, 1, size)
            )
            d = np.sqrt(x*x+y*y)
            kernel = np.exp(
                -(d**2 / (2.0*sigma**2))
            )
            kernel /= np.sum(kernel)
            self._convolve(kernel)

    def snr(self, image: Image) -> float:
        p_signal = np.sum(image.data ** 2)
        p_noise = np.sum((self.data - image.data) ** 2)
        return 10 * np.log10(p_signal / p_noise)