import numpy as np
import cv2
from mainCamera import MainCamera
from leftSideCamera import LeftSideCamera
from rightSideCamera import RightSideCamera
#import time

class DrivingProcessing:
    def __init__(self, w, h, camera):
        self.w = w
        self.h = h
        self.camera = camera
        self.left = False
        self.right = False
        self.forward = True
        self.error = False

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
                sideCamera = LeftSideCamera(np.array(frame))
                self.forward, self.left, self.right, self.error = sideCamera.capturingFunction()
            else:
                print("Wrong Camera Name!")
                break
            if self.error is not True:
                if self.left == True:
                    print("TURN LEFT.")
                elif self.right == True:
                    print("TURN RIGHT.")
                elif self.forward == True:
                    print("OK. Slope:")
            else:
                print("No lane detected.")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()