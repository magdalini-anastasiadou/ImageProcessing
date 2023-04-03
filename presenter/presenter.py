from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt

from typing import Protocol, Union, Callable


class Signal(Protocol):
    def connect(self, callback: Callable) -> None:
        pass

    def disconnect(self, callback: Callable) -> None:
        pass

    def emit(self, *args, **kwargs):
        pass


class View(Protocol):
    def set_image(self, image: Union[np.ndarray, None]) -> None:
        pass

    def set_plot(self, figure: Union[plt.figure, None]) -> None:
        pass

    def is_plot_visible(self) -> bool:
        pass


class Model(Protocol):
    image_changed: Signal

    def open_image(self, image_path: str) -> None:
        pass

    def get_image(self) -> Union[np.ndarray, None]:
        pass

    def save_image(self, image_path: str) -> None:
        pass

    def set_image(self, image: Union[np.ndarray, None]) -> None:
        pass

    def get_histogram_figure(self) -> Union[plt.figure, None]:
        pass


class Presenter:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.model.image_changed.connect(self.update_view)
        self.model.image_changed.connect(self.update_plot)
        self.view = view

    def handle_new_image(self):
        self.model.set_image(None)

    def handle_open_image(self, image_path: str):
        self.model.open_image(image_path)

    def handle_save_image(self, image_path: str):
        self.model.save_image(image_path)

    def update_view(self):
        image = self.model.get_image()
        self.view.set_image(image)

    def handle_show_histogram(self):
        figure = self.model.get_histogram_figure()
        self.view.set_plot(figure)

    def update_plot(self):
        if self.view.is_plot_visible():
            self.handle_show_histogram()