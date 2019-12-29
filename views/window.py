from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QSlider, QLabel, QComboBox, QSizePolicy, QScrollArea, QGroupBox, QFrame, QAction
from PyQt5.QtCore import Qt, QThread, QTimer
from PyQt5.QtGui import QPixmap
import numpy as np
from pyqtgraph import ImageView, GraphicsView
from pyqtgraph.widgets.RawImageWidget import RawImageWidget
import cv2
import os
from models.menu import Menu

class StartWindow(QMainWindow):
    def __init__(self, camera, movie, video):
        super().__init__()
        self.camera = camera
        self.movie = movie
        self.video = video
        self.framerate = 1000
        self.mode = 'camera'
        self.menu = Menu(self)
        self.menu.menu()

        self.central_widget = QWidget()
        self.central_widget.resizeEvent = self.on_resize
        # self.showMaximized()
        self.resize(1400, 1000)

        self.layout = QVBoxLayout(self.central_widget)
        self.controls()
        self.video_widget()
        self.frames_widget()

        self.setCentralWidget(self.central_widget)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.playback_handler)

        self.movie_thread = None


    def on_resize(self, event):
        self.movie_width = self.image_view.geometry().width()
        self.movie_height = self.image_view.geometry().height()

    def select_color(self):
        self.combo_box_color = QComboBox()
        self.combo_box_color.addItems(["Black & White", "Color", "BGR", "Yellow"])
        self.combo_box_color.currentIndexChanged.connect(self.set_color)
        self.combo_box_color.setCurrentIndex(1)
        return self.combo_box_color

    def set_color(self):
        color = self.combo_box_color.currentText()
        self.movie.set_color(color)
        self.camera.set_color(color)

    def video_widget(self):
        movie_view = QHBoxLayout()
        self.image_view = RawImageWidget()
        movie_view.addWidget(self.image_view)
        self.layout.addLayout(movie_view)

    def frames_widget(self):
        group = QGroupBox('Frames')
        lay = QHBoxLayout()
        group.setLayout(lay)
        frames = self.movie.get_frame_details()
        # TODO sort

        for frame_name in frames:
            fr_layout = QVBoxLayout()

            pixmap = QPixmap(frame_name)
            pixmap = pixmap.scaledToWidth(300) # TODO make sizeable
            pix_label = QLabel(frame_name)
            pix_label.setPixmap(pixmap)
            fr_layout.addWidget(pix_label)

            file_label = QLabel()
            file_label.setText(os.path.basename(frame_name))
            fr_layout.addWidget(file_label)

            lay.addLayout(fr_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidget(group)
        self.layout.addWidget(scroll_area)

    def controls(self):
        self.button_frame = QPushButton('Acquire Frame', self.central_widget)
        self.button_movie = QPushButton('Start/Stop Movie', self.central_widget)

        self.slider_framerate = QSlider(Qt.Horizontal)
        self.slider_framerate.setRange(1, 10)
        self.slider_framerate.setTickPosition(QSlider.TicksBelow)
        self.slider_framerate.setValue(self.framerate)
        self.label_framerate = QLabel()

        movie_controls = QHBoxLayout()
        movie_controls.addWidget(self.button_frame)
        movie_controls.addWidget(self.button_movie)
        self.toggle_mode_controls(movie_controls)
        movie_controls.addWidget(self.slider_framerate)
        movie_controls.addWidget(self.label_framerate)
        movie_controls.addWidget(self.select_color())

        self.layout.addLayout(movie_controls)

        self.button_frame.clicked.connect(self.write_image)
        self.button_movie.clicked.connect(self.start_stop_movie)
        self.slider_framerate.valueChanged.connect(self.update_framerate)
        self.label_framerate.setText("Frame Rate: {}".format(self.framerate))

    def write_image(self):
        frame = self.camera.get_raw_frame()
        file = "test.jpg"
        self.movie.write_frame(frame)

    def playback_handler(self):
        if self.mode == 'playback':
            return self.update_playback_frame()
        return self.update_movie()

    def update_movie(self):
        img = self.camera.get_frame()
        self.image_view.setImage(self.movie.size_image(img, self.movie_width, self.movie_height))

    def update_playback_frame(self):
        self.image_view.setImage(self.movie.get_frame(self.movie.playback_index, self.movie_width, self.movie_height))
        self.movie.playback_index += 1
        if  self.movie.playback_index > self.movie.get_movie_length() - 1:
            self.stop_movie()
            self.movie.playback_index = 0

    def update_framerate(self, value):
        restart = False
        if self.movie_thread:
            self.stop_movie()
            restart = True
        self.framerate = value * 100
        self.video.framerate = self.framerate
        self.label_framerate.setText("Frame Rate: {}".format(self.framerate))
        if restart:
            self.movie_thread.wait()
            self.start_movie()

    def start_stop_movie(self):
        if not self.movie_thread or self.movie_thread.isFinished():
            self.start_movie()
        else:
            self.stop_movie()

    def start_movie(self):
        self.movie_thread = MovieThread(self.camera)
        self.movie_thread.start()
        self.update_timer.start(self.framerate) # every <framerate> ms

    def stop_movie(self):
        self.movie_thread.quit()
        self.update_timer.stop()

    def toggle_mode_controls(self, control_layout):
        group = QGroupBox('Mode')
        layout = QHBoxLayout()
        group.setLayout(layout)

        button_camera_mode = QPushButton('Camera Mode', self.central_widget)
        button_camera_mode.clicked[bool].connect(self.toggle_mode)
        layout.addWidget(button_camera_mode)

        button_playback_mode = QPushButton('Playback Mode', self.central_widget)
        button_playback_mode.clicked[bool].connect(self.toggle_mode)
        layout.addWidget(button_playback_mode)

        self.label_mode = QLabel()
        self.label_mode.setText('Camera Mode')
        layout.addWidget(self.label_mode)

        control_layout.addWidget(group)

    def toggle_mode(self):
        self.label_mode.setText(self.sender().text())
        if self.sender().text() == 'Camera Mode':
            self.mode = 'camera'
            self.button_frame.setDisabled(False)
        if self.sender().text() == 'Playback Mode':
            self.mode = 'playback'
            self.button_frame.setDisabled(True)

    def close(self):
        self.image_view.close()

class MovieThread(QThread):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera

# if __name__ == '__main__':
#     app = QApplication([])
#     window = StartWindow()
#     window.show()
#     app.exit(app.exec_())
