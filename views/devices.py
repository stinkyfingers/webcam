from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from pyqtgraph.widgets.RawImageWidget import RawImageWidget
from models.movie import Movie

class DevicesModal():
    def __init__(self, camera, layout, close):
        self.camera = camera
        self.layout = layout
        self.close = close
        self.device_widget()

    def get_devices(self):
        cameras = self.camera.list_cameras()
        return cameras

    def device_widget(self):
        cameras = self.get_devices()
        self.h_layout = QHBoxLayout()
        camera_number = QLabel('Current Camera: {}'.format(self.camera.cam_num))
        self.h_layout.addWidget(camera_number)
        for camera_index, frame in cameras.items():
            v_layout = QVBoxLayout()
            image_view = RawImageWidget()
            image_view.setImage(Movie.size_image(frame, 200, 120))
            image_view.setFixedHeight(140)
            v_layout.addWidget(image_view)
            button = QPushButton()
            button.setFixedWidth(200)
            button.setText('Use Camera {}'.format(camera_index))
            button.clicked.connect(lambda state, i=camera_index: self.handle_device_change(i))
            v_layout.addWidget(button)
            self.h_layout.addLayout(v_layout)
        self.layout.addLayout(self.h_layout)

    def handle_device_change(self, index):
        self.camera.set_camera_number(index)
        self.close()
