import numpy as np
import cv2
from mainCamera import MainCamera
from sideCamera import SideCamera
from motorProcessing import MotorProcessing
import time

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
        motor = MotorProcessing(15, 22)
        while(True):
            _, frame = cap.read()
            if self.camera == "MainCamera":
                mainCamera = MainCamera(np.array(frame))
                self.forward, self.left, self.right = mainCamera.capturingFunction()
            elif self.camera == "SideCamera":
                sideCamera = SideCamera(np.array(frame))
                self.forward, self.left, self.right, self.error = sideCamera.capturingFunction()
            else:
                print("Wrong Camera Name!")
                break
            if self.error is not True:
                if self.left == True:
                    motor.motorFunc(False, True)
                    print("TURN LEFT.")
                elif self.right == True:
                    motor.motorFunc(True, False)
                    print("TURN RIGHT.")
                elif self.forward == True:
                    motor.motorFunc(False, False)
                    print("OK. Slope:")
            else:
                print("No lane detected.")
                motor.motorFunc(False, False)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                motor.motorFunc(False, False)
                break

        cap.release()
        cv2.destroyAllWindows()


