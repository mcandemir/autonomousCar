from imageProcessing import imageProcessing
from videoProcessing import videoProcessing
from simulationProcessing import SimulationProcessing

while(True):
    print("What do you want to do? (Image Processing:1, Simulation Processing: 2, Exit:0)")
    decision = int(input())
    if decision == 1:    
        imageName = "RoadPhotoWithSign.png"
        videoName = "RoadVideo_Trim1.mp4"
        imageProcessing = imageProcessing(imageName)
        imageProcessing.displayingScreen(imageName, imageProcessing.imageFunction())
        videoProcessing = videoProcessing(videoName)
        videoProcessing.videoFunction(15)
    elif decision == 2:
        print("Which camera do you use in the simulation (Main Camera:1, Side Camera: 2, Exit:0)")
        camera = int(input())
        if camera == 1:
            simulationProcessing = SimulationProcessing(225, 207, 1400, 900, "MainCamera")
        elif camera == 2:
            simulationProcessing = SimulationProcessing(271, 210, 575, 375, "SideCamera")
        elif camera == 0:
            break
        else:
            print("Wrong input!")
            break
        simulationProcessing.simulationFunction()
    elif decision == 0:
        break
    else:
        print("Wrong input!")
