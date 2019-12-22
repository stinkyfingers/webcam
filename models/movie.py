import cv2
import os
import numpy as np

# TODO dictionary of image location

class Movie:
    def __init__(self):
        self.dir = os.path.join(os.getcwd(), 'movie') # TODO rename project & project dir
        self.file_index = self.get_next_index()
        self.playback_index = 0
        self.colorspace = cv2.IMREAD_COLOR
        self.image_colorspace = cv2.COLOR_BGR2RGB
        self.colormap = {
            "Color": cv2.IMREAD_COLOR,
            "BGR": cv2.COLOR_BGR2RGB,
            "Black & White": cv2.COLOR_BGR2GRAY,
            "Yellow": cv2.COLOR_RGB2YUV
        }
        self.image_colormap = {
            "Color": cv2.COLOR_BGR2RGB,
            "BGR": cv2.IMREAD_COLOR,
            "Black & White": cv2.COLOR_BGR2GRAY,
            "Yellow": cv2.COLOR_RGB2YUV
        }
        if os.path.exists(self.dir) == False:
            os.mkdir(self.dir)

    def set_color(self, colorspace):
        if colorspace in self.colormap:
            self.colorspace = self.colormap[colorspace]
            self.image_colorspace = self.image_colormap[colorspace]

    def write_frame(self, frame):
        filename = "frame.{}.jpg".format(self.file_index)
        path = os.path.join(self.dir, filename)
        image = cv2.cvtColor(frame, self.colorspace)
        cv2.imwrite(path, image)
        self.file_index += 1

    def get_next_index(self):
        high = -1
        for file in os.listdir(self.dir):
            filename = os.fsdecode(file)
            print('---', filename)
            spl = filename.split('.')
            print(spl)
            if len(spl) < 3:
                continue #TODO malformed filename
            if int(spl[1]) > high:
                high = int(spl[1])
        return high + 1

    def get_frames(self, width, height):
        images = {}
        for file in os.listdir(self.dir):
            # TODO sort
            scale = .2
            raw_image = cv2.imread(os.path.join(self.dir, file))

            # rgb translate & rotate
            img = np.rot90(cv2.cvtColor(raw_image, self.image_colorspace))
            images[file] = self.size_image(img, width, height)
        return images

    def get_frame_details(self):
        files = []
        for file in os.listdir(self.dir):
            files.append(os.path.join(self.dir, file))
        return files

    def get_frame(self, index, width, height):
        # TODO handle sort
        file = os.listdir(self.dir)[index]
        scale = .2
        raw_image = cv2.imread(os.path.join(self.dir, file))

        # rgb translate & rotate
        img = np.rot90(cv2.cvtColor(raw_image, self.image_colorspace))
        output = self.size_image(img, width, height)
        return output

    def get_movie_length(self):
        return len(os.listdir(self.dir))
        
    @staticmethod
    def size_image(img, width, height):
        """
        scales image to fit smaller of width and height provided
        """
        w_scale = width/img.shape[0]
        h_scale = height/img.shape[1]
        scale = w_scale if w_scale < h_scale else h_scale # smaller of height & width
        dim = (int(img.shape[1] * scale), int(img.shape[0] * scale))
        return cv2.resize(img, dim)
