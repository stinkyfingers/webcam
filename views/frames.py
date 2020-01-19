from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QGroupBox, QLineEdit, QSlider
from PyQt5.QtGui import QPixmap, QTransform, QDrag
from PyQt5.QtCore import QMimeData, Qt, QEvent
import os
from models.video import Video
import sip

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QListWidget, QWidget, QApplication, QListWidgetItem, QAbstractItemView, QLabel, QLineEdit, QVBoxLayout


class Frames():
    def __init__(self, movie, layout):
        self.movie = movie
        self.layout = layout
        self.frame_size = 1
        self.frames = self.movie.get_frame_details()
        self.selected_frame = 0
        self.controls()

    def frames_widget(self):
        self.flw = FrameListWidget(None, self.frames, self.movie, self.layout, self.frame_size, self.update_project_frames, self.set_selected_frame_label)
        self.layout.addWidget(self.flw)

    def set_selected_frame_label(self, frame_index):
        self.selected_frame = frame_index
        if len(self.frames):
            self.current_frame_label.setText('Current Frame: {}'.format(os.path.basename(self.frames[self.selected_frame])))
        else:
            self.current_frame_label.setText('Current Frame: {}'.format('None'))

    def update_project_frames(self):
        self.layout.removeWidget(self.flw)
        self.frames = self.movie.get_frame_details()
        self.set_selected_frame_label(0)
        self.frames_widget()

    def add_frame(self, frame_name, index):
        self.frames.append(frame_name)
        self.flw.add_frame(frame_name, index)

    def update_frame_size(self, value):
        self.frame_size = value
        self.label_framesize.setText("Frame Size: {}".format(self.frame_size * 100))
        self.layout.removeWidget(self.flw)
        sip.delete(self.flw)
        self.flw = FrameListWidget(None, self.frames, self.movie, self.layout, self.frame_size, self.update_project_frames, self.set_selected_frame_label)
        self.layout.addWidget(self.flw)

    def controls(self):
        self.widget_framesize = QWidget()
        self.layout_framesize = QHBoxLayout()
        self.widget_framesize.resize(1,1)
        self.slider_framesize = QSlider(Qt.Horizontal)
        self.slider_framesize.setRange(1, 10)
        self.slider_framesize.setTickPosition(QSlider.TicksBelow)
        self.slider_framesize.setValue(self.frame_size)
        self.slider_framesize.valueChanged.connect(self.update_frame_size)
        self.label_framesize = QLabel()
        self.label_framesize.setText("Frame Size: {}".format(self.frame_size * 100))
        if len(self.frames):
            self.current_frame_label = QLabel('Current Frame: {}'.format(os.path.basename(self.frames[self.selected_frame])))
        else:
            self.current_frame_label = QLabel('Current Frame: {}'.format('None'))
        self.current_frame_label.setStyleSheet("background-color: #000; color: #eee; border: 1px inset grey; max-height: 15px;")
        self.layout_framesize.addWidget(self.current_frame_label)
        self.layout_framesize.addWidget(self.label_framesize)
        self.layout_framesize.addWidget(self.slider_framesize)
        self.widget_framesize.setLayout(self.layout_framesize)
        self.layout.addWidget(self.widget_framesize)

class FrameListWidget(QListWidget):
    def __init__(self, parent, frames, movie, layout, frame_size, update_project_frames, set_selected_frame_label):
        super(QListWidget, self).__init__(parent)
        self.setFlow(QListWidget.LeftToRight) #Horizontal
        self.setSpacing(0)
        self.frames = frames
        self.movie = movie
        self.layout = layout
        self.frame_size = frame_size
        self.update_project_frames = update_project_frames
        self.set_selected_frame_label = set_selected_frame_label
        self.set_frames_data()

    def set_frames_data(self):
        self.setDragDropMode(QAbstractItemView.InternalMove)
        list_model = self.model()
        list_model.rowsMoved.connect(self.on_layout_change)
        for i, frame_name in enumerate(sorted(self.frames, key = Video.sort_func)):
            item = QListWidgetItem(self)
            item_widget = FrameWidget(self, frame_name, i, self.movie, self.layout, self.frame_size, self.update_project_frames, self.set_selected_frame_label)
            item.setSizeHint(item_widget.sizeHint())
            self.addItem(item)
            self.setItemWidget(item, item_widget)

    def on_layout_change(self, moved, moved_i, moved_index, dest, dest_index):
        self.movie.shift_frames(moved_index, dest_index)
        self.update_project_frames()

    def add_frame(self, frame_name, index):
        item = QListWidgetItem(self)
        item_widget = FrameWidget(self, frame_name, index, self.movie, self.layout, self.frame_size, self.update_project_frames, self.set_selected_frame_label)
        item.setSizeHint(item_widget.sizeHint())
        self.addItem(item)
        self.setItemWidget(item, item_widget)

class FrameWidget(QWidget):
    def __init__(self, parent, frame_name, index, movie, layout, frame_size, update_project_frames, set_selected_frame_label):
        super(QWidget, self).__init__(parent)
        self.frame_name = frame_name
        self.index = index
        self.movie = movie
        self.layout = layout
        self.frame_size = frame_size
        self.update_project_frames = update_project_frames
        self.set_selected_frame_label = set_selected_frame_label
        self.set_frame_data()

    def set_frame_data(self):
        self.mouseReleaseEvent = self.selectFrame
        fr_layout = QVBoxLayout()
        pixmap = QPixmap(self.frame_name)
        pixmap = pixmap.scaledToWidth(self.frame_size * 100).transformed(QTransform().scale(-1, 1))
        pix_label = QLabel(self.frame_name)
        pix_label.setPixmap(pixmap)
        frame_name_label = QLabel(os.path.basename(self.frame_name))
        frame_name_label.setStyleSheet("background-color: #eee; max-height: 15px;")
        frame_name_label.setAlignment(Qt.AlignCenter)
        frame_name_label.setMargin(0)
        delete_button = QPushButton('Delete')
        delete_button.clicked.connect(lambda:self.delete_frame(self.index))
        fr_layout.addWidget(pix_label)
        fr_layout.addWidget(frame_name_label)
        fr_layout.addWidget(delete_button)
        self.setLayout(fr_layout)

    def delete_frame(self, index):
        self.movie.delete_frame(index)
        self.update_project_frames()

    def selectFrame(self, event):
        self.selected_frame = self.index
        self.set_selected_frame_label(self.index)
