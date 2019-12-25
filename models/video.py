import cv2
import os
import numpy as np

class Video:
    def __init__(self, movie, camera):
        self.movie = movie
        self.camera = camera
        self.dir = os.path.join(os.getcwd(), 'movie') # TODO rename project & project dir
        self.output_file = 'output.mp4' # TODO file name option

    def write_mpg(self):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        images = [img for img in os.listdir(self.dir) if img.endswith(".jpg")]
        frame = cv2.imread(os.path.join(self.dir, images[0]))
        height, width, layers = frame.shape # sample shape

        out = cv2.VideoWriter(self.output_file, fourcc, 1, (width, height)) #TODO 
        dirs = os.listdir(self.dir)

        for file in sorted(os.listdir(self.dir)):
            image_path = os.path.join(self.dir, file)
            image = cv2.imread(image_path)
            resized = cv2.resize(image, (width, height))
            out.write(resized)

        cv2.destroyAllWindows()
        out.release()
