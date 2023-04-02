import sys
from PyQt5.QtWidgets import QApplication

from model.model import Model
from presenter.presenter import Presenter
from view.view import ImageEditor


def main() -> None:
    app = QApplication([])
    model = Model()
    view = ImageEditor()
    presenter = Presenter(model, view)
    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()