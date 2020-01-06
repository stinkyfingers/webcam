from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QGroupBox, QLineEdit
from PyQt5.QtGui import QPixmap, QTransform, QDrag
from PyQt5.QtCore import QMimeData, Qt
import os

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QListWidget, QWidget, QApplication, QListWidgetItem, QAbstractItemView, QLabel, QLineEdit, QVBoxLayout


class Frames():
    def __init__(self, movie, layout):
        self.movie = movie
        self.layout = layout
        self.frames = self.movie.get_frame_details()
        self.selected_frame = 0
        self.selected_frame_label()

    def frames_widget(self):
        self.flw = FrameListWidget(None, self.frames, self.movie, self.layout, self.update_project_frames, self.set_selected_frame_label)
        self.layout.addWidget(self.flw)

    def selected_frame_label(self):
        self.current_frame_label = QLabel('Current Frame: {}'.format(os.path.basename(self.frames[self.selected_frame])))
        self.layout.addWidget(self.current_frame_label)

    def set_selected_frame_label(self, frame_index):
        self.selected_frame = frame_index
        self.current_frame_label.setText('Current Frame: {}'.format(os.path.basename(self.frames[self.selected_frame])))

    def update_project_frames(self):
        self.layout.removeWidget(self.flw)
        self.frames = self.movie.get_frame_details()
        self.set_selected_frame_label(0)
        self.frames_widget()

class FrameListWidget(QListWidget):
    def __init__(self, parent, frames, movie, layout, update_project_frames, set_selected_frame_label):
        super(QListWidget, self).__init__(parent)
        self.setFlow(QListWidget.LeftToRight) #Horizontal
        self.frames = frames
        self.movie = movie
        self.layout = layout
        self.update_project_frames = update_project_frames
        self.set_selected_frame_label = set_selected_frame_label
        self.set_frames_data()

    def set_frames_data(self):
        self.setDragDropMode(QAbstractItemView.InternalMove)
        for i, frame_name in enumerate(self.frames):
            item = QListWidgetItem(self)
            item_widget = FrameWidget(self, frame_name, i, self.movie, self.layout, self.update_project_frames, self.set_selected_frame_label)
            item.setSizeHint(item_widget.sizeHint())
            self.addItem(item)
            self.setItemWidget(item, item_widget)


class FrameWidget(QWidget):
    def __init__(self, parent, frame_name, index, movie, layout, update_project_frames, set_selected_frame_label):
        super(QWidget, self).__init__(parent)
        self.frame_name = frame_name
        self.index = index
        self.movie = movie
        self.layout = layout
        self.update_project_frames = update_project_frames
        self.set_selected_frame_label = set_selected_frame_label
        self.set_frame_data()

    def set_frame_data(self):
        self.mouseReleaseEvent = self.selectFrame
        fr_layout = QVBoxLayout()
        pixmap = QPixmap(self.frame_name)
        pixmap = pixmap.scaledToWidth(300).transformed(QTransform().scale(-1, 1)) # TODO make sizeable
        pix_label = QLabel(self.frame_name)
        pix_label.setPixmap(pixmap)
        fr_layout.addWidget(pix_label)
        frame_name_label = QLabel(os.path.basename(self.frame_name))
        frame_name_label.setAlignment(Qt.AlignCenter)
        delete_button = QPushButton('Delete')
        delete_button.clicked.connect(lambda:self.delete_frame(self.index))
        fr_layout.addWidget(frame_name_label)
        fr_layout.addWidget(delete_button)
        self.setLayout(fr_layout)

    def delete_frame(self, index):
        self.movie.delete_frame(index)
        self.update_project_frames()

    def selectFrame(self, event):
        self.selected_frame = self.index
        self.set_selected_frame_label(self.index)
