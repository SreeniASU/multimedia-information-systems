import cv2
import numpy as np
from os import listdir
from os.path import isfile,join
import Utility as util


def pc1 (yFrameValues):
    return yFrameValues

def pc2(yFrameValues):
    yFrameValues = yFrameValues.astype(float)
    result = np.zeros((10,10))
    print("Setting in initial value to ", yFrameValues[0,0])
    lastValue = yFrameValues[0,0]

    for i in range(0,10):
        for j in range (0,10):
            result[i][j] = abs(yFrameValues[i,j] - lastValue)
            lastValue = yFrameValues[i,j]

    return result

def pc3(yFrameValues):
    yFrameValues = yFrameValues.astype(float)
    result = np.zeros((10,10))
    print("Setting in initial values to ", yFrameValues[0,0], yFrameValues[0,1])

    for i in range(0,10):
        for j in range (0,10):
            previous_1 = yFrameValues[util.goBack(i,j,1,10)]
            previous_2 = yFrameValues[util.goBack(i,j,2,10)]
            predicted = (previous_1 + previous_2)/ 2
            result[i][j] = abs(yFrameValues[i,j] - predicted)

    return result


rootDir = "/Users/jake/Projects/multimedia-information-systems/test/project1" #util.safeGetDirectory()
allFiles = [f for f in listdir(rootDir) if isfile(join(rootDir,f))]
videoForProcessing = "3.mp4" # util.getVideoFile(allFiles)
x,y = util.getPixelRegion()
encodingOption = 3 #util.getEncodingOption()

videoName = rootDir + "/" + videoForProcessing
video = cv2.VideoCapture(videoName)

while(video.isOpened()):
    channels = 0
    ret,frame = video.read()
    if ret: #if video is still running...
        croppedFrame = frame[x:x+10, y:y+10]
        YCC_CroppedFrame = cv2.cvtColor(croppedFrame, cv2.COLOR_BGR2YCR_CB)
        yFrameValues = cv2.split(YCC_CroppedFrame)[0]
        print yFrameValues

        if encodingOption == 1:
            print pc1(yFrameValues)
        elif encodingOption == 2:
            print pc2(yFrameValues)
        elif encodingOption == 3:
            print pc3(yFrameValues)
        elif encodingOption == 4:
            print pc4(yFrameValues)


    else:
        break
