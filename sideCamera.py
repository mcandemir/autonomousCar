import numpy as np 
import cv2
import time
from PIL import ImageGrab
from imageProcessing import imageProcessing
from pynput.keyboard import Key, Controller

class SideCamera:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = None
        self.minX1 = None
        self.minY1 = None
        self.maxX2 = None
        self.maxY2 = None

    def capturingFunction(self):
        keyboard = Controller()
        img = ImageGrab.grab(bbox = (self.x, self.y, self.w, self.h))
        self.image = np.array(img)
        cv2.imshow("Line", self.image)
        white_image = imageProcessing.whiteDetection(self, self.image, 210, 255)
        canny_image = imageProcessing.canny(self, white_image)
        lines = cv2.HoughLinesP(canny_image, 2, np.pi/180, 100, np.array([]), minLineLength = 45, maxLineGap = 5)
        count = 0
        sumX = 0
        sumY = 0
        print(self.image.shape[0])
        for line in lines:
            count += 2
            x1, y1, x2, y2 = line.reshape(4)
            sumX += (x1 + x2)
            sumY += (y1 + y2) 
            #cv2.line(self.image,(x1,y1),(x2,y2), (255,255,0), 2)
        avgX = int(sumX / count)
        avgY = int(sumY / count)
        cv2.line(self.image, (0, int(self.image.shape[0] / 2)), (self.image.shape[1], int(self.image.shape[0] / 2)), (255, 0, 0), 2)
        cv2.line(self.image, (0, avgY), (self.image.shape[1], avgY), (255, 255, 0), 2)
        if int(self.image.shape[0] / 2) - 10 <= avgY <= int(self.image.shape[0] / 2):
            return True, False, False #F L R
        elif int(self.image.shape[0] / 2) - 10 > avgY:
            return False, True, False #F L R
        elif avgY > int(self.image.shape[0] / 2):
            return False, False, True #F L R
        #cv2.line(canny, ( int(lineCoordinate[0]), int(lineCoordinate[1])), (int(lineCoordinate[2]), int(lineCoordinate[3])), (255, 255, 0), 8)
        
        
"""

sample = SideCamera(271, 210, 575, 375)
sample.capturingFunction()"""