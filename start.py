from PyQt5.QtWidgets import QApplication

from models.camera import Camera
from views.window import StartWindow
from models.movie import Movie
from models.video import Video

camera = Camera(0)
camera.initialize()

movie = Movie()

video = Video(movie, camera)

app = QApplication([])
start_window = StartWindow(camera, movie, video)
start_window.show()
app.exit(app.exec_())
camera.set_brightness(camera.original_brightness)
