import cv2

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

    def initialize(self):
        self.cap = cv2.VideoCapture(self.cam_num)
        if not self.cap.isOpened():
            return -1
        # self.cap.set(cv2.CAP_PROP_MODE, cv2.IMREAD_COLOR)


    def get_frame(self):
        ret, self.last_frame = self.cap.read()

        # rgb translate
        frame = cv2.cvtColor(self.last_frame, self.colorspace)

        # rotate - https://www.tutorialkart.com/opencv/python/opencv-python-rotate-image/
        (h, w) = frame.shape[:2]
        center = (w / 2, h / 2)
        M = cv2.getRotationMatrix2D(center, 90, 1.0)
        rotated90 = cv2.warpAffine(frame, M, (h, w))
        return rotated90

    def get_raw_frame(self):
        """
        for use with imwrite() - for saving img to file
        """
        ret, frame = self.cap.read()
        # need vertical flip (mirror image)
        vert_flip = cv2.flip(frame, 1)
        return vert_flip

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
