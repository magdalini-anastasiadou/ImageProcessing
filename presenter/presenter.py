

class Presenter:
    def __init__(self, model, view):
        self.model = model
        self.model.image_changed.connect(self.update_view)
        self.model.image_changed.connect(self.update_plot)
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

    def handle_show_histogram(self):
        figure = self.model.get_histogram_figure()
        self.view.set_plot(figure)

    def update_plot(self):
        if self.view.is_plot_visible():
            self.handle_show_histogram()

    def handle_brightness_changed(self, brightness: float):
        self.model.set_attribute("brightness", brightness)

    def handle_contrast_changed(self, contrast: float):
        self.model.set_attribute("contrast", contrast)

    def handle_cancel(self):
        self.model.cancel()

    def handle_accept(self):
        self.model.accept()