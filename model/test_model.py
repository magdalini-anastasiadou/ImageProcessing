
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

