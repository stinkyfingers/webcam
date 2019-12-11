import cv2
import os

class Movie:
    def __init__(self):
        self.dir = os.path.join(os.getcwd(), 'movie') # TODO rename project & project dir
        self.file_index = self.get_next_index()
        self.colorspace = cv2.IMREAD_COLOR
        self.colormap = {
            "Color": cv2.IMREAD_COLOR,
            "BGR": cv2.COLOR_BGR2RGB,
            "Black & White": cv2.COLOR_BGR2GRAY,
            "Yellow": cv2.COLOR_RGB2YUV
        }
        if os.path.exists(self.dir) == False:
            os.mkdir(self.dir)

    def set_color(self, colorspace):
        if colorspace in self.colormap:
            self.colorspace = self.colormap[colorspace]

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
