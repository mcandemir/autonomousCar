import numpy as np
import cv2
import time
from PIL import ImageGrab
from imageProcessing import imageProcessing
from pynput.keyboard import Key, Controller

class capturingProcessing:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def capturingFunction(self):  
        time.sleep(10)
        keyboard = Controller()
        while(True):  
            keyboard.press('w')
            img = ImageGrab.grab(bbox = (self.x, self.y, self.w, self.h))
            img_np = np.array(img)
            imageProcessing.image = img_np
            cv2.imshow("Captured Frame", imageProcessing.imageFunction())
            if imageProcessing.slope < 0:
                print("TURN LEFT. Degree:", imageProcessing.slope)
                keyboard.press('a')
                time.sleep(0.08)
                keyboard.release('a')
            elif imageProcessing.slope > 0:
                print("TURN RIGHT. Degree:", imageProcessing.slope)
                keyboard.press('d')
                time.sleep(0.08)
                keyboard.release('d')
            elif imageProcessing.slope == 0:
                print("OK. Slope:", imageProcessing.slope)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            keyboard.release('w')

imageProcessing = imageProcessing()