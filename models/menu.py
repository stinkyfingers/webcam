from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMenu, QAction, QDialog, QPushButton, QLineEdit
import sys
import os
from models.config import Config

class Menu():
    def __init__(self, window):
        self.window = window

    def menu(self):
        self.main_menu = self.window.menuBar()
        self.main_menu.setNativeMenuBar(False)
        self.file_menu = self.main_menu.addMenu('&File')

        quit_option = QAction('&Quit', self.window)
        quit_option.setShortcut('Ctrl+Q')
        quit_option.triggered.connect(self.close_application)
        self.file_menu.addAction(quit_option)

        new_option = QAction('&New Project', self.window)
        new_option.setShortcut('Ctrl+N')
        new_option.triggered.connect(self.new_project)
        self.file_menu.addAction(new_option)

        export_option = QAction('&Export', self.window)
        export_option.setShortcut('Ctrl+E')
        export_option.triggered.connect(self.export)
        self.file_menu.addAction(export_option)

        import_menu = QMenu('&Import', self.main_menu)
        import_action = QAction('Import image', self.window)
        import_action.triggered.connect(self.import_image)
        import_menu.addAction(import_action)
        self.file_menu.addMenu(import_menu)

    def close_application(self):
        sys.exit()

    def new_project(self):
        dialog = NewProjectDialog()
        dialog.show()

    def export(self):
        self.window.video.write_mpg()

    def import_image(self):
        print("not implemented")

class NewProjectDialog():
    def __init__(self):
        self.dialog = QDialog()

    def show(self):
        self.textbox = QLineEdit(self.dialog)
        self.textbox.move(50, 10)
        self.textbox.resize(200, 20)

        self.ok = QPushButton('ok', self.dialog)
        self.ok.move(50, 30)
        self.ok.clicked.connect(self.create_project)

        self.cancel = QPushButton('cancel', self.dialog)
        self.cancel.move(100, 30)
        self.cancel.clicked.connect(self.dialog.reject)

        self.dialog.setWindowTitle('Project Name')
        self.dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        self.dialog.exec_()

    def create_project(self, text):
        project = self.textbox.text() # TODO app dir
        if not os.path.isdir(project): # TODO select existing project
            os.mkdir(project)
        config = Config()
        config.upsert({'project': project})
        self.dialog.accept()
