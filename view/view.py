from PyQt5.QtWidgets import QMainWindow, QApplication, QAction
from PyQt5.QtGui import QIcon


class ImageEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Image Editor")
        self.setWindowIcon(QIcon("view/icons/colour.png"))
        self.create_file_menu()
        self.create_edit_menu()
        self.create_adjust_menu()
        self.create_view_menu()
        self.set_window_style()
        self.showMaximized()

    def create_file_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')

        new_file_action = QAction('New File', self)
        new_file_action.setShortcut('Ctrl+N')
        file_menu.addAction(new_file_action)

        open_file_action = QAction('Open File...', self)
        open_file_action.setShortcut('Ctrl+O')
        file_menu.addAction(open_file_action)

        save_file_action = QAction('Save', self)
        save_file_action.setShortcut('Ctrl+S')
        file_menu.addAction(save_file_action)
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def create_edit_menu(self):
        menu_bar = self.menuBar()
        edit_menu = menu_bar.addMenu('Edit')

        undo_action = QAction('Undo', self)
        undo_action.setShortcut('Ctrl+Z')
        undo_action.setEnabled(False)
        edit_menu.addAction(undo_action)

        redo_action = QAction('Redo', self)
        redo_action.setShortcut('Ctrl+Y')
        redo_action.setEnabled(False)
        edit_menu.addAction(redo_action)
    
    def create_adjust_menu(self):
        menu_bar = self.menuBar()
        adjust_menu = menu_bar.addMenu('Adjust')

        gray_scale_action = QAction('Auto B&&W', self)
        adjust_menu.addAction(gray_scale_action)

        brightness_action = QAction('Brightness', self)
        adjust_menu.addAction(brightness_action)

    def create_view_menu(self):
        menu_bar = self.menuBar()
        view_menu = menu_bar.addMenu('View')

        histogram_action = QAction('Histogram', self)
        histogram_action.setEnabled(False)
        view_menu.addAction(histogram_action)

    def set_window_style(self):
        with open('view/stylesheet.qss') as f:
            app = QApplication.instance()
            stylesheet = f.read()
            app.setStyleSheet(stylesheet)
