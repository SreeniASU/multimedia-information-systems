__author__ = 'Team 6'

import Utility as util
import cv2
import numpy as np
import time
from os import listdir
from os.path import isfile,join


def pc1(outputFile,yFrameValues, frameNum):
    totalAbsoluteError = 0
    writeToFile(outputFile, yFrameValues, frameNum, totalAbsoluteError)

def pc2(outputFile,yFrameValues, frameNum):
    totalAbsoluteError = 0

    yFrameValues = yFrameValues.astype(float)
    result = np.zeros((10,10))
    previousValue = 0

    for i in range(0,10):
        for j in range (0,10):
            if j-1>=0:
                result[i][j] = yFrameValues[i,j] - yFrameValues[i,j-1]
                totalAbsoluteError = totalAbsoluteError + abs(result[i][j])
            else:
                result[i][j] = yFrameValues[i,j]
    writeToFile(outputFile, result, frameNum, totalAbsoluteError)


def pc3(outputFile,yFrameValues, frameNum):
    totalAbsoluteError = 0
    yFrameValues = yFrameValues.astype(float)
    result = np.zeros((10,10))

    for i in range(0,10):
        for j in range (0,10):
            if i-1>=0:
                result[i][j] = yFrameValues[i,j] - yFrameValues[i-1,j]
                totalAbsoluteError = totalAbsoluteError + abs(result[i][j])
            else:
                result[i][j] = yFrameValues[i,j]
    writeToFile(outputFile, result, frameNum, totalAbsoluteError)

def pc4(outputFile,yFrameValues, frameNum):
    totalAbsoluteError = 0
    yFrameValues = yFrameValues.astype(float)
    result = np.zeros((10,10))

    for i in range(0,10):
        for j in range (0,10):
            if i-1>=0 and j-1>=0:
                result[i][j] = yFrameValues[i,j] - yFrameValues[i-1,j-1]
                totalAbsoluteError  = totalAbsoluteError  + abs(result[i][j])
            else:
                result[i][j] = yFrameValues[i,j]
    writeToFile(outputFile, result, frameNum, totalAbsoluteError)

def pc5(outputFile,yFrameValues, frameNum):
    totalAbsoluteError = 0
    yFrameValues = yFrameValues.astype(float)
    result = np.zeros((10,10))
    for i in range(0,10):
        for j in range(0,10):
            if i-1>=0 and j-1>=0:
                result[i][j] = yFrameValues[i,j] - \
                               ( yFrameValues[i-1,j-1]/float(3) +  yFrameValues[i-1,j]/float(3) +  yFrameValues[i,j-1]/float(3))
                totalAbsoluteError  = totalAbsoluteError  + abs(result[i][j])
            elif i-1>=0:
                result[i][j] = yFrameValues[i,j] - yFrameValues[i-1,j]
                totalAbsoluteError  = totalAbsoluteError  + abs(result[i][j])
            elif j-1>=0:
                result[i][j] = yFrameValues[i,j] - yFrameValues[i,j-1]
                totalAbsoluteError  = totalAbsoluteError  + abs(result[i][j])
            else:
                result[i][j] = yFrameValues[i,j]
    writeToFile(outputFile, result, frameNum, totalAbsoluteError)


def writeToFile(file, values, frameNum, error):
    rows = len(values)
    cols = len(values[0])
    for i in range(rows):
        for j in range(cols):
            contents = "< f" + str(frameNum) + ",(" + str(i) + "," + str(j) + "), " + str(values[i][j]) + " >\n"

            file.write(contents)


    totalAbsoluteErrorContent = "Total Absolute Error for this frame is " + str(error) + "\n"
    file.write(totalAbsoluteErrorContent)

# Directory in which all the video files are pesent
print('Enter root directory')

rootDir = "D:\\VideoFiles"

# Get all the files from the root directory
allFiles = [f for f in listdir(rootDir) if isfile(join(rootDir,f))]

print(allFiles)

#Get the video for processing
videoName = raw_input('Enter the video file you want to process')
#ToDo : User input should be provided
videoForProcessing = rootDir + "\\" + videoName

option = util.getEncodingOption()
x,y = util.getPixelRegion()

fileName = videoForProcessing.strip('.mp4') + "_" + option + ".spc"
outputFile = open(fileName, 'w')

#Get all the frames from the video
video = cv2.VideoCapture(videoForProcessing)
ret, frame = video.read()
framesList = []
frameNum = 0
while(video.isOpened()):
    ret, frame = video.read()
    if ret:
        frameNum +=1

        croppedFrame = frame[x:x+10, y:y+10]
        YCC_CroppedFrame = cv2.cvtColor(croppedFrame, cv2.COLOR_BGR2YCR_CB)
        yFrameValues = cv2.split(YCC_CroppedFrame)[0]
        if option == "1":
            pc1(outputFile, yFrameValues, frameNum)
        elif option == "2":
            pc2(outputFile, yFrameValues, frameNum)
        elif option == "3":
            pc3(outputFile, yFrameValues, frameNum)
        elif option == "4":
            pc4(outputFile, yFrameValues, frameNum)
        elif option == "5":
            pc5(outputFile, yFrameValues, frameNum)
    else:
        break
time.sleep(1)
outputFile.close()

