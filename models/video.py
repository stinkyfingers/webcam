import cv2
import os
import numpy as np
from models.config import Config

class Video:
    def __init__(self, movie, camera):
        self.movie = movie
        self.camera = camera
        c = Config()
        self.dir = os.path.join(os.getcwd(), c.get_project_dir())
        self.output_file = 'output.mp4' # TODO file name option
        self.framerate = 1000

    def write_mpg(self):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        images = [img for img in os.listdir(self.dir) if img.endswith(".jpg")]
        frame = cv2.imread(os.path.join(self.dir, images[0]))
        height, width, layers = frame.shape # sample shape

        out = cv2.VideoWriter(self.output_file, fourcc, 1000/self.framerate, (width, height)) #TODO
        dirs = os.listdir(self.dir)

        for file in sorted(os.listdir(self.dir), key = self.sort_func):
            image_path = os.path.join(self.dir, file)
            image = cv2.imread(image_path)
            resized = cv2.resize(image, (width, height))
            out.write(resized)

        cv2.destroyAllWindows()
        out.release()
        return self.output_file

    @staticmethod
    def sort_func(s):
        arr = s.split('.')
        if len(arr) < 2 or not isinstance(int(arr[1]), int):
            return -1
        return int(arr[1])
