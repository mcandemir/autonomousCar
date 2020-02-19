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
        self.left = False
        self.right= False
        self.forward = True

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
                self.left = True
                self.right = False
                self.forward = False
            elif imageProcessing.slope > 0:
                self.right = True
                self.left = False
                self.forward = False
            elif imageProcessing.slope == 0:
                self.right = False
                self.left = False
                self.forward = True
            if self.left == True:
                keyboard.release('d')
                print("TURN LEFT. Degree:", imageProcessing.slope)
                keyboard.press('a')
            if self.right == True:
                keyboard.release('a')
                print("TURN RIGHT. Degree:", imageProcessing.slope)
                keyboard.press('d')
            if self.forward == True:
                keyboard.release('a')
                keyboard.release('d')
                print("OK. Slope:", imageProcessing.slope)
            keyboard.release('w')
            if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
imageProcessing = imageProcessing()