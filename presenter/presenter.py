from __future__ import annotations
import numpy as np

from typing import Protocol, Union


class View(Protocol):
    def set_image(self, image: Union[np.ndarray, None]) -> None:
        pass


class Model(Protocol):
    def open_image(self, image_path: str) -> None:
        pass

    def get_image(self) -> Union[np.ndarray, None]:
        pass

    def save_image(self, image_path: str) -> None:
        pass

    def set_image(self, image: Union[np.ndarray, None]) -> None:
        pass


class Presenter:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view

    def handle_new_image(self):
        self.model.set_image(None)
        self.update_view()

    def handle_open_image(self, image_path: str):
        self.model.open_image(image_path)
        self.update_view()

    def handle_save_image(self, image_path: str):
        self.model.save_image(image_path)

    def update_view(self):
        image = self.model.get_image()
        self.view.set_image(image)