from PyQt5.QtWidgets import QSlider, QLabel, QPushButton, QHBoxLayout, QGroupBox, QComboBox
from PyQt5.QtCore import Qt

# TODO finish and implement

class Controls():
    def __init__(self, central_widget, layout, video, movie, camera, scroll_area):
        self.central_widget = central_widget
        self.layout = layout
        self.framerate = 1000
        self.video = video
        self.movie = movie
        self.camera = camera
        self.scroll_area = scroll_area

    def display(self):
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

    def write_image(self):
        frame = self.camera.get_raw_frame()
        filename = self.movie.write_frame(frame)
        self.add_frame(filename, self.movie.get_next_index())
        self.scroll_area.setWidget(self.frames_group)
