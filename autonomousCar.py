from imageProcessing import imageProcessing
from videoProcessing import videoProcessing

imageName = "RoadPhotoWithSign.png"
videoName = "RoadVideo_Trim1.mp4"
imageProcessing = imageProcessing(imageName)
imageProcessing.displayingScreen(imageName, imageProcessing.imageProcess())
videoProcessing = videoProcessing(videoName)
videoProcessing.videoProcess(15)
