import numpy as np
import cv2
import time
from mainCamera import MainCamera
from sideCamera import SideCamera
from pynput.keyboard import Key, Controller

class SimulationProcessing:
    def __init__(self, x, y, w, h, camera):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.camera = camera
        self.left = False
        self.right = False
        self.forward = True

    def simulationFunction(self):
        keyboard = Controller()
        time.sleep(5)
        while(True):
            keyboard.press('w')
            if self.camera == "MainCamera":
                mainCamera = MainCamera(self.x, self.y, self.w, self.h)
                self.forward, self.left, self.right = mainCamera.capturingFunction()
            elif self.camera == "SideCamera":
                sideCamera = SideCamera(self.x, self.y, self.w, self.h)
                self.forward, self.left, self.right = sideCamera.capturingFunction()
            if self.left == True:
                keyboard.release('d')
                print("TURN LEFT.")
                keyboard.press('a')
            if self.right == True:
                keyboard.release('a')
                print("TURN RIGHT.")
                keyboard.press('d')
            if self.forward == True:
                keyboard.release('a')
                keyboard.release('d')
                print("OK. Slope:")
            if keyboard.press('q') == True:
                    break
        cv2.destroyAllWindows()
        keyboard.release('w')
                