from imageProcessing import ImageProcessing
from videoProcessing import VideoProcessing
from simulationProcessing import SimulationProcessing
from drivingProcessing import DrivingProcessing

while(True):
    print("What do you want to do? (Image & Video Processing: 1, Simulation Processing: 2, Driving: 3, Exit: 0)")
    decision = int(input())
    if decision == 1:
        imageName = "RoadPhotoWithSign.png"
        videoName = "RoadVideo_Trim1.mp4"
        imageProcessing = ImageProcessing(imageName)
        imageProcessing.displayingScreen(imageName, imageProcessing.imageFunction())
        videoProcessing = VideoProcessing(videoName)
        videoProcessing.videoFunction()
    elif decision == 2:
        print("Which camera do you use in the simulation (Main Camera:1, Side Camera: 2, Exit:0)")
        camera = int(input())
        if camera == 1:
            simulationProcessing = SimulationProcessing(225, 207, 1400, 900, "MainCamera", 1160, 240, 1465, 390)
        elif camera == 2:
            simulationProcessing = SimulationProcessing(271, 210, 575, 375, "SideCamera",1160, 240, 1465, 390)
        elif camera == 0:
            break
        else:
            print("Wrong input!")
            break
        simulationProcessing.simulationFunction()
    elif decision == 3:
        print("Which camera do you use in the driving? (Main Camera:1, Side Camera: 2, Exit:0)")
        camera = int(input())
        if camera == 1:
            drivingProcessing = DrivingProcessing(1280, 720, "MainCamera")
        elif camera == 2:
            drivingProcessing = DrivingProcessing(1280, 720, "SideCamera")
        elif camera == 0:
            break
        else:
            print("Wrong Input!")
            break
        drivingProcessing.drivingFunction()
    elif decision == 0:
        break
    else:
        print("Wrong input!")
