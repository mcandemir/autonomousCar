import numpy as np
import cv2
from mainCamera import MainCamera
from sideCamera import SideCamera
import time

class DrivingProcessing:
    def __init__(self, w, h, camera):
        self.w = w
        self.h = h
        self.camera = camera
        self.left = False
        self.right = False
        self.forward = True

    def drivingFunction(self):
        cap = cv2.VideoCapture(1)
        cap.set(3, self.w)
        cap.set(4, self.h)
        while(True):
            _, frame = cap.read()
            if self.camera == "MainCamera":
                mainCamera = MainCamera(np.array(frame))
                self.forward, self.left, self.right = mainCamera.capturingFunction()
            elif self.camera == "SideCamera":
                sideCamera = SideCamera(np.array(frame))
                self.forward, self.left, self.right = sideCamera.capturingFunction()
            else:
                print("Wrong Camera Name!")
                break
            if self.left == True:
                print("TURN LEFT.")
            if self.right == True:
                print("TURN RIGHT.")
            if self.forward == True:
                print("OK. Slope:")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()