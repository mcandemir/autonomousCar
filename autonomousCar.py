from imageProcessing import imageProcessing
from videoProcessing import videoProcessing
from capturingProcessing import capturingProcessing

imageName = "RoadPhotoWithSign.png"
videoName = "RoadVideo_Trim1.mp4"
imageProcessing = imageProcessing(imageName)
imageProcessing.displayingScreen(imageName, imageProcessing.imageFunction())
videoProcessing = videoProcessing(videoName)
videoProcessing.videoFunction(15)
capturingProcessing = capturingProcessing(225, 207, 1400, 720)
capturingProcessing.capturingFunction()
