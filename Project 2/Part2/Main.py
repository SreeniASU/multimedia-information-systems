__author__ = 'Sreenivas'

import Utility as util
import cv2
import numpy as np
from os import listdir
from os.path import isfile,join

def pc1(yFrameValues):
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
    print("Setting in initial value to ", yFrameValues[0,0])
    lastValue = yFrameValues[0,0]

    for i in range(0,10):
        for j in range (0,10):
            result[j][i] = abs(yFrameValues[j,i] - lastValue)
            lastValue = yFrameValues[j,i]
    return result

def pc4(yFrameValues):
    yFrameValues = yFrameValues.astype(float)
    result = np.zeros((10,10))
    print("Setting an initial value to ", yFrameValues[0,0])
    lastValue = yFrameValues[0,0]

    for i in range(0,10):
        for j in range (0,10):
            if i+1 < 10 and j+1 < 10:
                result[i][j] = abs(yFrameValues[i+1, j+1] - lastValue )
                lastValue = yFrameValues[i,j]
            else:
                result[i][j] = yFrameValues[i, j]
    return result


def writeToFile(file, values, frameNum):
    rows = len(values)
    cols = len(values[0])
    for i in range(rows):
        for j in range(cols):
            contents = "< f" + str(frameNum) + ",(" + str(i) + "," + str(j) + "), " + str(values[i][j]) + " >\n"
            file.write(contents)

# Directory in which all the video files are present
print('Enter root directory');
# ToDo: User input should be provided
rootDir = "D:\\VideoFiles";

# Get all the files from the root directory
allFiles = [f for f in listdir(rootDir) if isfile(join(rootDir,f))]

print(allFiles)

#Get the video for processing
print('Enter the video file you wan to process')
#ToDo : User input should be provided
videoForProcessing = "3.mp4"

option = util.getEncodingOption()
x,y = util.getPixelRegion()

fileName = videoForProcessing.strip('.mp4') + "_" + option + ".tpc"
outputFile = open(fileName, 'w')

#Get all the frames from the video
video = cv2.VideoCapture(videoForProcessing)
ret, frame = video.read()
framesList = []
frameNum = 0;
while(video.isOpened()):
    ret, frame = video.read()
    if ret:
        frameNum +=1
        croppedFrame = frame[x:x+10, y:y+10]
        YCC_CroppedFrame = cv2.cvtColor(croppedFrame, cv2.COLOR_BGR2YCR_CB)
        yFrameValues = cv2.split(YCC_CroppedFrame)[0]

        if option == "1":
            writeToFile(outputFile, pc1(yFrameValues), frameNum)
        elif option == "2":
            writeToFile(outputFile, pc2(yFrameValues), frameNum)

        framesList.append(croppedFrame)


