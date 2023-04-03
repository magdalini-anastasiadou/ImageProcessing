

class Presenter:
    def __init__(self, model, view):
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