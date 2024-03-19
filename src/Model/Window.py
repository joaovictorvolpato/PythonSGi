from utils import consts


class Window:
    def __init__(self):
        self.xw_min = consts.VIEWPORT_X_MIN
        self.yw_min = consts.VIEWPORT_Y_MIN
        self.xw_max = consts.VIEWPORT_X_MAX
        self.yw_max = consts.VIEWPORT_Y_MAX

        self.step = 10  # amount of pixels
        self.rotation_zoom_percentage = 10
