import numpy as np
import cv2
import time
from mainCamera import MainCamera
from leftSideCamera import LeftSideCamera
from rightSideCamera import RightSideCamera
from pynput.keyboard import Key, Controller
from pynput.mouse import Controller as MouseController
from PIL import ImageGrab
import pyautogui

class SimulationProcessing:
    def __init__(self, camera, xR, yR, wR, hR):
        self.x = None
        self.y = None
        self.x2 = None
        self.y2 = None
        self.xR = xR
        self.yR = yR
        self.x2R = wR
        self.y2R = hR
        self.camera = camera
        self.left = False
        self.right = False
        self.forward = True
        self.errorLeft = False
        self.errorRight = False
        self.activity = "None"

    def gettingMouseAxis(self):
            print("Proceeding...")
            print("Point the left top corner of the left camera")
            time.sleep(5)
            mouse = MouseController()
            x, y = mouse.position
            self.x = int(x)
            self.y = int(y)
            print("Point the right bottom corner of the left camera")
            time.sleep(3)
            x, y = mouse.position
            self.x2 = int(x)
            self.y2 = int(y)
            print("Point the left top corner of the right camera")
            time.sleep(3)
            x, y = mouse.position
            self.xR = int(x)
            self.yR = int(y)
            print("Point the right bottom corner of the right camera")
            time.sleep(3)
            x, y = mouse.position
            self.x2R = int(x)
            self.y2R = int(y)
            print("All done!")

    def simulationFunction(self):
        self.gettingMouseAxis()
        keyboard = Controller()
        while(True):
            img = ImageGrab.grab((self.x, self.y, self.x2, self.y2))
            if self.camera == "MainCamera":
                mainCamera = MainCamera(np.array(img))
                self.forward, self.left, self.right = mainCamera.capturingFunction()
            elif self.camera == "SideCamera":
                sideCamera = LeftSideCamera(np.array(img))
                self.forward, self.left, self.right,self.errorLeft = sideCamera.capturingFunction()
                if self.errorLeft is False:
                    sideCamera = LeftSideCamera(np.array(img))
                    self.forward, self.left, self.right,self.errorLeft = sideCamera.capturingFunction()
                else:
                    img1 = ImageGrab.grab((self.xR, self.yR, self.x2R, self.y2R))
                    rightSideCamera = RightSideCamera(np.array(img1))
                    self.forward, self.left, self.right, self.errorRight = rightSideCamera.capturingFunction()
                if self.errorLeft and self.errorRight is True:
                    self.activity = "None"
                elif self.errorLeft is False and self.errorRight is not True:
                    self.activity = "Left"
                else:
                    self.activity = "Right"
            if self.camera == "MainCamera":
                keyboard.press('w')
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
                    print("OK Slope")
            elif self.camera == "SideCamera":
                if self.activity == "None":
                    keyboard.release('w')
                    keyboard.release('a')
                    keyboard.release('d')
                    print("No lane detected..")
                else:
                    keyboard.press('w')
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
                        print("OK Slope.")
                #keyboard.release('w')
            if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        cv2.destroyAllWindows()
        keyboard.release('w')