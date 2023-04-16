
import pytest
import numpy as np

from model.model import Model
from model.processing import Image

class TestModel:
    @pytest.fixture
    def model(self):
        model = Model()
        model.open_file("model/files/DSC00032.jpg")
        return model

    def test_accept(self, model):
        data = model.image.data
        model.set_attribute("brightness", 100)
        assert np.equal(model.image.data, data).all()
        assert len(model._edit_actions) == 1
        model.accept()
        assert np.equal(model.image.data, data).all()
        assert len(model._edit_actions) == 2
    
    def test_cancel(self, model):
        data = model.image.data
        assert len(model._edit_actions) == 0
        model.set_attribute("brightness", 100)
        assert np.equal(model.image.data, data).all()
        assert len(model._edit_actions) == 1
        model.set_attribute("contrast", 10)
        assert np.equal(model.image.data, data).all()
        assert len(model._edit_actions) == 2
        model.cancel()
        assert np.equal(model.image.data, data).all()
        assert len(model._edit_actions) == 0


class TestImage:
    @pytest.fixture
    def image(self):
        red = np.random.randint(0, 256, size=(100, 100, 3), dtype=np.uint8)
        green = np.random.randint(0, 256, size=(100, 100, 3), dtype=np.uint8)
        blue = np.random.randint(0, 256, size=(100, 100, 3), dtype=np.uint8)
        data = np.dstack((red, green, blue))
        return Image(data)

    def test_brightness(self, image):
        data = image.data
        mean_red = np.mean(data[:, :, 0])
        mean_green = np.mean(data[:, :, 1])
        mean_blue = np.mean(data[:, :, 2])
        image.set_brightness(100)
        data = image.data
        assert np.mean(data[:, :, 0]) > mean_red
        assert np.mean(data[:, :, 1]) > mean_green
        assert np.mean(data[:, :, 2]) > mean_blue
    
    def test_contrast(self, image):
        data = image.data
        variance = np.var(data)
        image.set_contrast(10)
        data = image.data
        assert np.var(data) > variance