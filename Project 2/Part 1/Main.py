import cv2
import numpy as np
from os import listdir
from os.path import isfile,join
import Utility as util


rootDir = "#/home/perry/Desktop/Project 2" #util.safeGetDirectory()
#allFiles = [f for f in listdir(rootDir) if isfile(join(rootDir,f))]
videoForProcessing = "3.mp4" #util.getVideoFile(allFiles)
x,y = util.getPixelRegion()
#encodingOption = util.getEncodingOption()

video = cv2.VideoCapture(videoForProcessing)

while(video.isOpened()):
    channels = 0
    ret,frame = video.read()
    if ret: #if video is still running...
        croppedFrame = frame[x:x+10, y:y+10]
        YCC_CroppedFrame = cv2.cvtColor(croppedFrame, cv2.COLOR_BGR2YCrCb)
        yFrameValues = cv2.split(YCC_CroppedFrame)[0]

        i,j = 0
        for i in range(0,9):
            for j in range (0,9):
                frame[i,j]
    else:
        break