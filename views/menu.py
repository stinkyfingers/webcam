from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMenu, QAction, QDialog, QPushButton, QLineEdit, QFileDialog, QHBoxLayout, QLabel, QVBoxLayout, QLineEdit
import sys
import os
from models.config import Config
from views.devices import DevicesModal

class Menu():
    def __init__(self, window, project_change_callback):
        self.window = window
        self.project_change_callback = project_change_callback

    def set_camera(self, camera):
        self.camera = camera

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

        open_option = QAction('&Open Project', self.window)
        open_option.setShortcut('Ctrl+O')
        open_option.triggered.connect(self.open_project)
        self.file_menu.addAction(open_option)

        export_option = QAction('&Export', self.window)
        export_option.setShortcut('Ctrl+E')
        export_option.triggered.connect(self.export)
        self.file_menu.addAction(export_option)

        import_menu = QMenu('&Import', self.main_menu)
        import_action = QAction('Import image', self.window)
        import_action.triggered.connect(self.import_image)
        import_menu.addAction(import_action)
        self.file_menu.addMenu(import_menu)

        camera_action = QAction('Camera', self.window)
        camera_action.setShortcut('Ctrl+C')
        camera_action.triggered.connect(self.select_camera)
        self.file_menu.addAction(camera_action)

    def close_application(self):
        sys.exit()

    def new_project(self):
        dialog = NewProjectDialog(self.project_change_callback)
        dialog.show()

    def open_project(self):
        dialog = OpenProjectDialog()
        dialog.show(self.project_change_callback)

    def export(self):
        ExportDialog(self.window.video).show()
        file = self.window.video.write_mpg()
        ExportCompleteDialog(file).show()

    def import_image(self):
        print("not implemented")

    def select_camera(self):
        dialog = SelectCameraDialog(self.camera)
        dialog.show()

class NewProjectDialog():
    def __init__(self, project_change_callback):
        self.dialog = QDialog()
        self.project_change_callback = project_change_callback

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
        self.project_change_callback()
        self.dialog.accept()

class OpenProjectDialog():
    def __init__(self):
        self.dialog = QFileDialog()
        self.dialog.setFileMode(QFileDialog.Directory)

    def show(self, project_change_callback):
        self.dialog.exec_()
        project = self.dialog.selectedFiles()[0]
        config = Config()
        config.upsert({'project': project})
        project_change_callback()
        self.dialog.accept()

class SelectCameraDialog():
    def __init__(self, camera):
        self.dialog = QDialog()
        self.camera = camera

    def show(self):
        self.layout = QHBoxLayout()
        self.dialog.setLayout(self.layout)
        devices = DevicesModal(self.camera, self.layout, self.dialog.close)
        self.dialog.exec_()

class ExportCompleteDialog():
    def __init__(self, output_file):
        self.dialog = QDialog()
        self.output_file = output_file

    def show(self):
        close = QPushButton("Close")
        close.clicked.connect(self.dialog.close)
        text = QLabel("Export complete: {}".format(self.output_file))
        layout = QVBoxLayout()
        layout.addWidget(text)
        layout.addWidget(close)
        self.dialog.setLayout(layout)
        self.dialog.exec_()

class ExportDialog():
    def __init__(self, video):
        self.dialog = QDialog()
        self.video = video

    def show(self):
        button = QPushButton("OK")
        button.clicked.connect(self.dialog.close)
        label = QLabel("Export as:")
        text = QLineEdit()
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(text)
        layout.addWidget(button)
        self.dialog.setLayout(layout)
        self.dialog.exec_()
        filename = text.text()
        if not filename.endswith(".mp4"):
            filename = filename + ".mp4"
        self.video.output_file = filename
