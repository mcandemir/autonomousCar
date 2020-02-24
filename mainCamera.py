import numpy as np
from PIL import ImageGrab
from imageProcessing import imageProcessing

class MainCamera:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def capturingFunction(self):
        img = ImageGrab.grab((self.x, self.y, self.w, self.h))
        img_np = np.array(img)
        imageProcessing.image = img_np
        imageProcessing.showingScreen("Captured Frame", imageProcessing.imageFunction())
        if imageProcessing.slope < 0:
            return False, True, False #F L R
        if imageProcessing.slope > 0:
            return False, False, True #F L R
        if imageProcessing.slope == 0:
            return True, False, False #F L R

imageProcessing = imageProcessing()