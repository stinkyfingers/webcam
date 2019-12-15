from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QSlider, QLabel, QComboBox, QSizePolicy
from PyQt5.QtCore import Qt, QThread, QTimer
import numpy as np
from pyqtgraph import ImageView, GraphicsView
from pyqtgraph.widgets.RawImageWidget import RawImageWidget
import cv2


class StartWindow(QMainWindow):
    def __init__(self, camera, movie):
        super().__init__()
        self.camera = camera
        self.movie = movie
        self.framerate = 1000
        self.central_widget = QWidget()
        self.central_widget.resizeEvent = self.on_resize
        self.showMaximized()

        self.layout = QVBoxLayout(self.central_widget)
        self.controls()
        self.video_widget()
        self.frames_widget()

        self.setCentralWidget(self.central_widget)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_movie)

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
        frames_view = QHBoxLayout()

        frames = self.movie.get_frames(300)
        for frame_name in frames:
            fr_layout = QVBoxLayout()
            label = QLabel()
            label.setText(frame_name)
            fr_layout.addWidget(label)
            frame_view = RawImageWidget()
            frame_view.setImage(frames[frame_name])
            fr_layout.addWidget(frame_view)
            frames_view.addLayout(fr_layout)

        self.layout.addLayout(frames_view)

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

    def update_movie(self):
        img = self.camera.get_frame()
        w_scale = self.movie_width/img.shape[0]
        h_scale = self.movie_height/img.shape[1]
        scale = w_scale if w_scale < h_scale else h_scale # smaller of height & width
        dim = (int(img.shape[1] * scale), int(img.shape[0] * scale))
        self.image_view.setImage(cv2.resize(img, dim))

    def update_framerate(self, value):
        self.stop_movie()
        self.framerate = value * 100
        self.label_framerate.setText("Frame Rate: {}".format(self.framerate))
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
