import cv2
import numpy as np

class Camera:
    def __init__(self, cam_num):
        self.cam_num = cam_num
        self.cap = None
        self.original_brightness = 1
        self.colorspace = cv2.COLOR_BGR2RGB
        self.colormap = {
            "Color": cv2.COLOR_BGR2RGB,
            "BGR": cv2.IMREAD_COLOR,
            "Black & White": cv2.COLOR_BGR2GRAY,
            "Yellow": cv2.COLOR_RGB2YUV
        }
        self.last_frame = None
        self.ratio = 16/9 #TODO

    def initialize(self):
        self.cap = cv2.VideoCapture(self.cam_num)
        if not self.cap.isOpened():
            return -1

    def set_aspect_ratio(self, ratio):
        self.ratio = ratio

    def crop(self, frame):
        width = frame.shape[0]
        height = frame.shape[1]
        ratio = self.ratio
        if width/height > ratio:
            new_width = height*ratio
            new_w_start = int((width - new_width)/2)
            new_w_end = int(new_width + ((width - new_width)/2))
            frame = frame[new_w_start: new_w_end, 0:height]

        if width/height < ratio:
            new_height = width/ratio
            new_h_start = int((height - new_height)/2)
            new_h_end = int(new_height + ((height - new_height)/2))
            frame = frame[0:width, new_h_start:new_h_end]
        return frame

    def get_frame(self):
        _, frame = self.cap.read()
        # rotate
        frame = np.rot90(frame)
        #crop
        self.last_frame = self.crop(frame)
        # rgb translate
        frame = cv2.cvtColor(self.last_frame, self.colorspace)
        return frame

    def get_writable_last_frame(self):
        if self.last_frame is None:
            return None
        return np.rot90(self.last_frame, 3)

    def set_brightness(self, value):
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, value)

    def get_brightness(self):
        return self.cap.get(cv2.CAP_PROP_BRIGHTNESS)

    def set_color(self, colorspace):
        if colorspace in self.colormap:
            self.colorspace = self.colormap[colorspace]

    def close_camera(self):
        self.cap.release()

    def __str__(self):
        return 'OpenCV Camera {}'.format(self.cam_num)

    def list_cameras(self):
        index = 0
        arr = {}
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.read()[0]:
                break
            else:
                _, frame = cap.retrieve()
                frame = np.rot90(frame)
                frame = self.crop(frame)
                frame = cv2.cvtColor(frame, self.colorspace)
                arr[index] = frame
            cap.release()
            index += 1
        return arr

    def set_camera_number(self, index):
        self.cam_num = index
        self.initialize()
