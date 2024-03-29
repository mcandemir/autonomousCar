import numpy as np
import cv2
import time
from trafficSignProcessing import TrafficSign
from imageProcessing import ImageProcessing
from securityProcessing import SecurityProcessing
from mainCamera import MainCamera
from leftSideCamera import LeftSideCamera
from rightSideCamera import RightSideCamera
from pynput.keyboard import Key, Controller
from pynput.mouse import Controller as MouseController
from PIL import ImageGrab
import pyautogui
#import win32api
from Xlib import display

class SimulationProcessing:
    def __init__(self,camera):
        self.camera = camera
        self.left = False
        self.right = False
        self.forward = True
        self.errorLeft = False
        self.errorRight = False
        self.activity = "None"
        self.frameCount = 0
        self.Left_avgY = -1
        self.Right_avgY = -1
        #-------------------------
        self.leftLaneCheck = [1,1,1]
        self.rightLaneCheck = [1,1,1]
        self.leftAllOne = 1
        self.leftAllZero = 0
        self.rightAllOne = 1
        self.rightAllZero = 0
        self.missionRightTurn = False
        self.missionRightTurn_done = False
        self.missionLeftTurn = False
        self.missionLeftTurn_done = False
        #-------------------------
        """
        0-Sola dönülmez
        1-Sağa dönülmez
        2-İleri ve sola mecburi yön
        3-İleri ve sağa mecburi yön
        4-Sola dön
        5-Sağa Dön
        6-Taşıt trafiğine kapalı yol
        7-Durak bin
        8-Durak in
        9-Trafik lambası -1 yok 0-kırmızı 1-yeşil
        10-Dur
        """
        #-------------------------
        self.found_best = False
        self.LLC = False
        self.RLC = False
        self.brake = False
        self.brakeForStop = False
        self.brakeForStop_inArea = False
        self.brakeForDur = False
        self.brakeForDur_inArea = False

    """def click_coordinates(self):
        for pos in range(2):
            state_prev = win32api.GetKeyState(0x01)
            while True:
                state_current = win32api.GetKeyState(0x01)
                if state_current != state_prev:
                    pos = pyautogui.position()
                    print("**Positions set: ", pos)
                    return pos"""

    def set_pos(self):
        print("Set the area to process")
        print("Upper corner")
        time.sleep(2)
        mouseCoord = display.Display().screen().root.query_pointer()._data
        print(mouseCoord["root_x"], mouseCoord["root_y"])
        mouse_posX1, mouse_posY1 = mouseCoord["root_x"], mouseCoord["root_y"]
        print("Lower corner")
        time.sleep(2)
        mouseCoord = display.Display().screen().root.query_pointer()._data
        print(mouseCoord["root_x"], mouseCoord["root_y"])
        mouse_posX2, mouse_posY2 = mouseCoord["root_x"], mouseCoord["root_y"]
        self.x = int(mouse_posX1)
        self.y = int(mouse_posY1)
        self.w = int(mouse_posX2)
        self.h = int(mouse_posY2)

    def simulationFunction(self):
        self.set_pos()
        trafficSign = TrafficSign()
        avgOfCams = int((self.h - self.y)/2)
        keyboard = Controller()
        sensor = SecurityProcessing()
        leftSideCamera = LeftSideCamera()
        rightSideCamera = RightSideCamera()
        time.sleep(3)
        while(True):
            self.frameCount += 1
            wholeScreen = ImageGrab.grab((self.x, self.y, self.w, self.h))
            if self.camera == "MainCamera":
                mainCamera = MainCamera(np.array(wholeScreen))
                self.forward, self.left, self.right = mainCamera.capturingFunction()
            elif self.camera == "SideCamera":
                leftLineImg = wholeScreen.crop((0, 0, wholeScreen.size[0] * 0.25, wholeScreen.size[1] * 0.25))
                self.forward, self.left, self.right,self.errorLeft, self.Left_avgY = leftSideCamera.capturingFunction(np.array(leftLineImg))
                #bu verilerle asagıdakiler çakışıyor(rightSideCamera'nın fonksiyonundan atanan degerler, 4 satır aşağısı) o yüzden bunları değişkende tutacagız
                t_forward, t_left, t_right = self.forward, self.left, self.right
                rightLineImg = wholeScreen.crop((wholeScreen.size[0] * 0.75, 0, wholeScreen.size[0], wholeScreen.size[1] * 0.25))
                self.forward, self.left, self.right, self.errorRight, self.Right_avgY = rightSideCamera.capturingFunction(np.array(rightLineImg))
                
                """
                signsImg = wholeScreen.crop((wholeScreen.size[0] * 0.13, wholeScreen.size[1] * 0.29, wholeScreen.size[0] * 0.89, wholeScreen.size[1] * 0.95))
                signsImg = np.array(signsImg)
                points = self.gettingTrafficSignsUICoordinates(signsImg)

                sensorImg = wholeScreen.crop((wholeScreen.size[0] * 0.5, 0, wholeScreen.size[0] * 0.67, wholeScreen.size[1] * 0.24))
                sensorPoints = sensor.processFunc(np.array(sensorImg))
                print(sensorPoints)"""

                if self.errorLeft is False:
                    self.leftLaneCheck[self.frameCount%3] = 1
                    if self.leftLaneCheck[0] == 1 and self.leftLaneCheck[1] == 1 and self.leftLaneCheck[2] == 1:
                        self.leftAllOne = 1
                        if self.leftAllZero != 0:
                            self.missionRightTurn = True
                            self.missionRightTurn_done = True
                            self.leftAllZero = 0
                        else:
                            self.missionRightTurn = False
                else:
                    self.leftLaneCheck[self.frameCount%3] = 0
                    if self.leftLaneCheck[0] == 0 and self.leftLaneCheck[1] == 0 and self.leftLaneCheck[2] == 0:
                        self.leftAllZero = 1
                        if self.leftAllOne != 0:
                            self.missionRightTurn = True
                            self.missionRightTurn_done = True
                            self.leftAllOne = 0
                        else:
                            self.missionRightTurn = False
                if self.errorRight is False:
                    self.rightLaneCheck[self.frameCount%3] = 1
                    if self.rightLaneCheck[0] == 1 and self.rightLaneCheck[1] == 1 and self.rightLaneCheck[2] == 1:
                        self.rightAllOne = 1
                        if self.rightAllZero != 0:
                            self.missionLeftTurn = True
                            self.missionLeftTurn_done = True
                            self.rightAllZero = 0
                        else:
                            self.missionLeftTurn = False
                else:
                    self.rightLaneCheck[self.frameCount%3] = 0
                    if self.rightLaneCheck[0] == 0 and self.rightLaneCheck[1] == 0 and self.rightLaneCheck[2] == 0:
                        self.rightAllZero = 1
                        if self.rightAllOne != 0:
                            self.missionLeftTurn = True
                            self.missionLeftTurn_done = True
                            self.rightAllOne = 0
                        else:
                            self.missionLeftTurn = False

                if self.missionRightTurn == True:
                    print("Left Lane change!!")
                    self.LLC = True
                if self.missionLeftTurn == True:
                    print("Right Lane change!!")
                    self.RLC = True
                
                greenColorRGB = [86,188,106]
                redColorRGB = [255,0,0]
                self.activity = "forward"
                
                """self.controllingTrafficSignStatus(trafficSign, signsImg, points, greenColorRGB, redColorRGB)
                trafficSign.printingAllSigns()"""

                if trafficSign.trafficLightStatus() == -1 or trafficSign.trafficLightStatus() == 1:
                    if self.brake is True:
                        keyboard.release(Key.space)
                        keyboard.press('s')
                        time.sleep(0.2)
                        keyboard.release('s')
                        self.brake = False
                    if trafficSign.trafficLightStatus() == 1:
                        if self.frameCount %4 == 0:
                            print("GREEN LIGHT!")
                    if self.brakeForStop_inArea == True and (trafficSign.passengerInStatus() == 1 or trafficSign.passengerOutStatus() == 1):
                        print("STOP!")
                        self.brakeForStop = True
                        self.activity = "Stop"
                    if self.brakeForDur_inArea == True and trafficSign.stopStatus() == 1:
                        print("Dur!")
                        self.brakeForDur = True
                        self.activity = "Dur"
                    if self.brakeForStop == False and self.brakeForDur is False:
                        if trafficSign.notLeftStatus() == 0 and trafficSign.notRightStatus() == 0:
                            if self.errorLeft is True and self.errorRight is True:
                                self.activity = "None"
                            elif self.errorLeft is True and self.errorRight is False:
                                self.activity = "Right"
                            elif self.errorLeft is False and self.errorRight is True:
                                self.forward, self.left, self.right = t_forward, t_left, t_right
                                self.activity = "Left"
                            elif self.errorLeft is False and self.errorRight is False:
                                if abs(avgOfCams - self.Left_avgY) <=  abs(avgOfCams - self.Right_avgY):
                                    self.forward, self.left, self.right = t_forward, t_left, t_right
                                    self.activity = "Left"
                                else:
                                    self.activity = "Right"
                        else:
                            if  trafficSign.notLeftStatus() == 1 and trafficSign.notRightStatus() == 0:
                                if self.frameCount %4 == 0:
                                    print("LEFT TURN FORBIDDEN")
                                if self.errorRight is False:
                                    self.activity = "Right"
                                    if (abs(abs(avgOfCams - self.Left_avgY) - abs(avgOfCams - self.Right_avgY)) <= 20 ) and self.missionRightTurn_done is True:
                                        print("Turning Right Done!")
                                        self.missionRightTurn_done = False
                                        trafficSign.trafficSignArray[0] = 0
                                else:
                                    self.activity = "None"
                            elif trafficSign.notRightStatus() == 1 and trafficSign.notLeftStatus() == 0:
                                if self.frameCount %4 == 0:
                                    print("RIGHT TURN FORBIDDEN")
                                if self.errorLeft is False:
                                    self.forward, self.left, self.right = t_forward, t_left, t_right
                                    self.activity = "Left"
                                    if (abs(abs(avgOfCams - self.Left_avgY) - abs(avgOfCams - self.Right_avgY)) <= 20 ) and self.missionLeftTurn_done is True:
                                        print("Turning Left Done!")
                                        self.missionLeftTurn_done = False
                                        trafficSign.trafficSignArray[1] = 0
                                else:
                                    self.activity = "None"
                            elif trafficSign.notRightStatus() == 1 and trafficSign.notLeftStatus() == 1:
                                #SIKINTILI İŞ SENSÖRLE OLMALI
                                if self.frameCount %4 == 0:
                                    print("LEFT AND RIGHT TURN FORBIDDEN")
                                if (abs(abs(avgOfCams - self.Left_avgY) - abs(avgOfCams - self.Right_avgY)) <= 15 ) and self.found_best is False:
                                    self.found_best = True
                                if self.found_best is True:
                                    self.left = False
                                    self.right = False
                                    self.forward = True
                                    self.activity = "forward"
                                    if (self.RLC is True) and (self.LLC is True):
                                        if self.errorLeft is False or self.errorRight is False:
                                            if abs(avgOfCams - self.Left_avgY) <= 20 or abs(avgOfCams - self.Right_avgY) <=20:
                                                print("Way Found Back!")
                                                trafficSign.trafficSignArray[1] = 0 
                                                trafficSign.trafficSignArray[0] = 0
                                                self.found_best = False
                                                self.LLC = False
                                                self.RLC = False
                                        
                elif trafficSign.trafficLightStatus() == 0 or trafficSign.trafficLightStatus() == 1:
                    if trafficSign.trafficLightStatus() == 1:
                        if self.frameCount %4 == 0:
                            print("RED LIGHT!")
                    else:
                        if self.frameCount %4 == 0:
                            print("YELLOW LIGHT!")
                    #freezing işlemi gelecek buraya
                    self.activity = "Brake"
                    self.brake = True
                



            if self.camera is "MainCamera":
                self.throttleActive(keyboard)
                if self.left == True:
                    self.turnLeft(keyboard)
                if self.right == True:
                    self.turnRight
                if self.forward == True:
                    self.goForward(keyboard)
            elif self.camera is "SideCamera":
                if self.activity is "None":
                    self.noAction(keyboard)
                elif self.activity is "Brake":
                    self.braking(keyboard)
                elif self.activity is "Stop":
                    self.stopping(keyboard)
                elif self.activity is "Dur":
                   self.dur(keyboard)
                else:
                    self.throttleActive(keyboard)
                    if self.left == True:
                        self.turnLeft(keyboard)
                    if self.right == True:
                        self.turnRight(keyboard)
                    if self.forward == True:
                        self.goForward(keyboard)
                #self.throttlePassive(keyboard)
            
            #keyboard.release('p')

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
        self.throttlePassive(keyboard)

    """def gettingTrafficSignsUICoordinates(self, image):
        initialXRatio = -0.024
        array = []
        for i in range(11):
            initialXRatio = initialXRatio + 0.091
            array.append([int(np.size(image, 0) * 0.5), int(initialXRatio * np.size(image, 1))])#y, x
        return array"""
    """
    def controllingTrafficSignStatus(self, trafficSign, image, points, greenColor, redColor):
        for i in range(11):
            if i == 9:
                trafficSign.trafficSignArray[i] = ImageProcessing.colorTesting(self, image[points[i][0], points[i][1]], greenColor, redColorRGB = redColor, isItTrafficLight = True)
            else:
                trafficSign.trafficSignArray[i] = ImageProcessing.colorTesting(self, image[points[i][0], points[i][1]], greenColor, isItTrafficLight = False)
        print(trafficSign.trafficSignArray)
        """

    def throttleActive(self, keyboard):
        keyboard.press('w')
    
    def throttlePassive(self, keyboard):
        keyboard.release('w')

    def turnLeft(self, keyboard):
        keyboard.release('d')
        print("TURN LEFT.")
        keyboard.press('a')

    def turnRight(self, keyboard):
        keyboard.release('a')
        print("TURN RIGHT.")
        keyboard.press('d')
    
    def goForward(self, keyboard):
        keyboard.release('a')
        keyboard.release('d')
        print("OK Slope")

    def noAction(self, keyboard):
        keyboard.release('w')
        keyboard.release('a')
        keyboard.release('d')
    
    def braking(self, keyboard):
        keyboard.release('w')
        keyboard.release('a')
        keyboard.release('d')
        keyboard.release('s')
        keyboard.press(Key.space)

    def stopping(self, keyboard):
        keyboard.release('w')
        keyboard.release('a')
        keyboard.release('d')
        keyboard.release('s')
        keyboard.press(Key.space)
        time.sleep(8)
        keyboard.release(Key.space)
        keyboard.press('s')
        time.sleep(0.2)
        keyboard.release('s')
        self.brakeForStop = False
        self.brakeForStop_inArea = False

    def dur(self, keyboard):
        keyboard.release('w')
        keyboard.release('a')
        keyboard.release('d')
        keyboard.release('s')
        keyboard.press(Key.space)
        time.sleep(8)
        keyboard.release(Key.space)
        keyboard.press('s')
        time.sleep(0.2)
        keyboard.release('s')
        self.brakeForDur = False
        self.brakeForDur_inArea = False