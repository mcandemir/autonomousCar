import numpy as np
from imageProcessing import ImageProcessing

class RightSideCamera:
    def __init__(self, image):
        self.image = image
        self.minX1 = None
        self.minY1 = None
        self.maxX2 = None
        self.maxY2 = None

    def capturingFunction(self):
        white_image = ImageProcessing.whiteDetection(self, self.image, 210, 255)
        canny_image = ImageProcessing.canny(self, white_image)
        lines = ImageProcessing.cHoughLinesP(self, canny_image, 45, 5)
        count = 0
        sumX = 0
        sumY = 0
        if lines is not None:
            for line in lines:
                count += 2
                x1, y1, x2, y2 = line.reshape(4)
                sumX += (x1 + x2)
                sumY += (y1 + y2)
            #avgX = int(sumX / count)
            avgY = int(sumY / count)
            ImageProcessing.showingLines(self, self.image, 0, int(self.image.shape[0] / 2), self.image.shape[1], int(self.image.shape[0] / 2), 255, 0, 0)
            ImageProcessing.showingLines(self, self.image, 0, avgY, self.image.shape[1], avgY, 255, 255, 0)
            ImageProcessing.showingScreen(self, "Line", self.image)
            print(self.image.shape)
            if int(self.image.shape[0] / 2) - 5 <= avgY <= int(self.image.shape[0] / 2):
                return True, False, False, False #F L R E
            if int(self.image.shape[0] / 2) - 5 > avgY:
                return False, False, True, False #F L R E
            if avgY > int(self.image.shape[0] / 2):
                return False, True, False, False #F L R E
        else:
            return  False, False, False, True #F L R E
