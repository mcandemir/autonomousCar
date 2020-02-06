import numpy as np
import cv2
from PIL import ImageGrab
from imageProcessing import imageProcessing

class capturingProcessing:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def capturingFunction(self):  
        while(True):  
            img = ImageGrab.grab(bbox = (self.x, self.y, self.w, self.h))
            img_np = np.array(img)
            imageProcessing.image = img_np
            cv2.imshow("asd", imageProcessing.imageFunction())
            if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

imageProcessing = imageProcessing()