from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QGroupBox
from PyQt5.QtGui import QPixmap, QTransform
import os

class Frames():
    def __init__(self, movie, layout):
        self.movie = movie
        self.layout = layout

        self.frames = self.movie.get_frame_details()
        self.selected_frame = 0

    def frames_widget(self):
        self.frames_v_layout = QVBoxLayout()
        self.current_frame_label = QLabel('Current Frame: {}'.format(os.path.basename(self.frames[self.selected_frame])))
        self.frames_v_layout.addWidget(self.current_frame_label)
        self.frames_group = QGroupBox('Frames')
        self.frame_layout = QHBoxLayout()
        self.frames_group.setLayout(self.frame_layout)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        for i, frame_name in enumerate(self.frames):
            self.add_frame(frame_name, i)
        self.scroll_area.setWidget(self.frames_group)
        self.frames_v_layout.addWidget(self.scroll_area)
        self.layout.addLayout(self.frames_v_layout)


    def add_frame(self, frame_name, index):
        fr_layout = QVBoxLayout()
        pixmap = QPixmap(frame_name)
        pixmap = pixmap.scaledToWidth(300).transformed(QTransform().scale(-1, 1)) # TODO make sizeable
        pix_label = QLabel(frame_name)
        pix_label.setPixmap(pixmap)
        fr_layout.addWidget(pix_label)
        file_button = QPushButton(os.path.basename(frame_name))
        file_button.clicked.connect(lambda:self.mouse_handler(index))
        delete_button = QPushButton('Delete')
        delete_button.clicked.connect(lambda:self.delete_frame(index))
        fr_layout.addWidget(file_button)
        fr_layout.addWidget(delete_button)
        self.frame_layout.addLayout(fr_layout)

    def mouse_handler(self, index):
        self.selected_frame = index
        self.current_frame_label.setText('Current Frame: {}'.format(os.path.basename(self.frames[self.selected_frame])))

    def delete_frame(self, index):
        self.current_frame_label.clear()
        self.movie.delete_frame(index)
        self.layout.removeItem(self.frames_v_layout)
        self.frames = self.movie.get_frame_details()
        self.frames_widget()

    def update_project_frames(self):
        self.current_frame_label.clear()
        self.layout.removeItem(self.frames_v_layout)
        self.frames = self.movie.get_frame_details()
        self.frames_widget()
