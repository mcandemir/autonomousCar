import numpy as np
from imageProcessing import imageProcessing

class SideCamera:
    def __init__(self, image):
        self.image = None
        self.minX1 = None
        self.minY1 = None
        self.maxX2 = None
        self.maxY2 = None

    def capturingFunction(self):
        white_image = imageProcessing.whiteDetection(self, self.image, 210, 255)
        canny_image = imageProcessing.canny(self, white_image)
        lines = imageProcessing.cHoughLinesP(self, canny_image, 45, 5)
        count = 0
        sumX = 0
        sumY = 0
        for line in lines:
            count += 2
            x1, y1, x2, y2 = line.reshape(4)
            sumX += (x1 + x2)
            sumY += (y1 + y2)
        #avgX = int(sumX / count)
        avgY = int(sumY / count)
        imageProcessing.showingLines(self, self.image, 0, int(self.image.shape[0] / 2), self.image.shape[1], int(self.image.shape[0] / 2), 255, 0, 0)
        imageProcessing.showingLines(self, self.image, 0, avgY, self.image.shape[1], avgY, 255, 255, 0)
        imageProcessing.showingScreen(self, "Line", self.image)
        print(self.image.shape)
        if int(self.image.shape[0] / 2) - 5 <= avgY <= int(self.image.shape[0] / 2):
            return True, False, False #F L R
        if int(self.image.shape[0] / 2) - 5 > avgY:
            return False, True, False #F L R
        if avgY > int(self.image.shape[0] / 2):
            return False, False, True #F L R
