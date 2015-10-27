__author__ = 'Team 6'

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
    print("Setting in initial value to 0")
    lastValue = 0

    for i in range(0,10):
        for j in range (0,10):
            result[i][j] = abs(yFrameValues[i,j] - lastValue)
            lastValue = yFrameValues[i,j]
        lastValue = 0
    return result

def pc3(yFrameValues):
    yFrameValues = yFrameValues.astype(float)
    result = np.zeros((10,10))
    print("Setting in initial value to 0")
    lastValue = 0

    for i in range(0,10):
        for j in range (0,10):
            result[j][i] = abs(yFrameValues[j,i] - lastValue)
            lastValue = yFrameValues[j,i]
        lastValue = 0;
    return result

def pc4(yFrameValues):
    yFrameValues = yFrameValues.astype(float)
    result = np.zeros((10,10))
    print("Setting an initial value to 0")
    lastValue = 0

    for i in range(0,10):
        for j in range (0,10):
            result[i][j] = yFrameValues[i][j] - lastValue
            if i-1>=0  and j-1 >=0:
	        lastValue = yFrameValues[i-1][j-1]
            else:
                lastValue = 0
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

fileName = videoForProcessing.strip('.mp4') + "_" + option + ".spc"
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
        #print yFrameValues
        #break
        if option == "1":
            writeToFile(outputFile, pc1(yFrameValues), frameNum)
        elif option == "2":
            writeToFile(outputFile, pc2(yFrameValues), frameNum)
        elif option == "3":
            writeToFile(outputFile, pc3(yFrameValues), frameNum)
        elif option == "4":
            writeToFile(outputFile, pc4(yFrameValues), frameNum)
print "End of code"




