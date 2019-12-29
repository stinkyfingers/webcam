from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMenu, QAction
import sys

class Menu():
    def __init__(self, window):
        self.window = window

    def menu(self):
        self.main_menu = self.window.menuBar()
        self.main_menu.setNativeMenuBar(False)
        self.file_menu = self.main_menu.addMenu('&File')

        quit_option = QAction('&Quit', self.window)
        quit_option.setShortcut("Ctrl+Q")
        quit_option.triggered.connect(self.close_application)
        self.file_menu.addAction(quit_option)

        export_option = QAction('&Export', self.window)
        export_option.setShortcut("Ctrl+E")
        export_option.triggered.connect(self.export)
        self.file_menu.addAction(export_option)

        import_menu = QMenu('&Import', self.main_menu)
        import_action = QAction('Import image', self.window)
        import_action.triggered.connect(self.import_image)
        import_menu.addAction(import_action)
        self.file_menu.addMenu(import_menu)

    def close_application(self):
        sys.exit()

    def export(self):
        self.window.video.write_mpg()

    def import_image(self):
        print("not implemented")
