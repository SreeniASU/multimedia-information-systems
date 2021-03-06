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
            contents = "<" + str(frameNum) + "," + str(i) + "," + str(j) + "," + str(values[i][j]) + "\n"

            file.write(contents)

    totalAbsoluteErrorContent = "Total Absolute Error for this frame is " + str(error) + "\n"
    file.write(totalAbsoluteErrorContent)

def spatialCoding(video, x, y, option, outputFile):
    #Get all the frames from the video
    print("Running spatial predictive coding " + option + "...")
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

if __name__ == '__main__':
    # Directory in which all the video files are pesent
    rootDir = util.safeGetDirectory()

    # Get all the files from the root directory
    allFiles = [f for f in listdir(rootDir) if isfile(join(rootDir,f))]

    #Get the video for processing
    videoName = util.getVideoFile(allFiles)
    videoForProcessing = join(rootDir, videoName)

    option = util.getEncodingOption()
    x,y = util.getPixelRegion()

    fileName = videoName.strip('.mp4') + "_" + option + ".spc"
    outputFile = open(fileName, 'w')
    video = cv2.VideoCapture(videoForProcessing)

    spatialCoding(video, outputFile)
