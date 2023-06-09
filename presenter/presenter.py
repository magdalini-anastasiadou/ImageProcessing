

class Presenter:
    def __init__(self, model, view):
        self.model = model
        self.model.image_changed.connect(self.update_view)
        self.view = view

    def handle_new_image(self):
        self.model.clear()

    def handle_open_file(self, fname: str):
        self.model.open_file(fname)

    def handle_save_file(self, fname: str):
        self.model.save_file(fname)

    def update_view(self):
        data = self.model.get_data()
        self.view.set_data(data)

    def handle_brightness_changed(self, brightness: float):
        self.model.set_attribute("brightness", brightness)

    def handle_contrast_changed(self, contrast: float):
        self.model.set_attribute("contrast", contrast)

    def handle_rotate_left(self):
        self.model.set_attribute("rotate", 90)

    def handle_rotate_right(self):
        self.model.set_attribute("rotate", -90)

    def handle_flip_horizontally(self):
        self.model.set_attribute("flip_horizontally", None)

    def handle_flip_vertically(self):
        self.model.set_attribute("flip_vertically", None)

    def handle_cancel(self):
        self.model.cancel()

    def handle_accept(self):
        self.model.accept()

    def handle_cancel_accept(self):
        self.model.cancel_accept()

    def handle_gaussian_blur(self, value: int):
        self.model.set_attribute("gaussian_blur", value)

    def handle_sharpen(self, value: int):
        self.model.set_attribute("sharpen", value)