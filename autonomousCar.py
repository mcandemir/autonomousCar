from imageProcessing import imageProcessing
from videoProcessing import videoProcessing
from simulationProcessing import SimulationProcessing
"""
imageName = "RoadPhotoWithSign.png"
videoName = "RoadVideo_Trim1.mp4"
imageProcessing = imageProcessing(imageName)
imageProcessing.displayingScreen(imageName, imageProcessing.imageFunction())
videoProcessing = videoProcessing(videoName)
videoProcessing.videoFunction(15)
"""
#simulationProcessing = SimulationProcessing(225, 207, 1400, 900, "MainCamera")
simulationProcessing = SimulationProcessing(271, 210, 575, 375, "SideCamera")
simulationProcessing.simulationFunction()
