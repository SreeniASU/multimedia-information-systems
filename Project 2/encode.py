__author__ = "Team 6"

import cv2
import os.path
import sys
import numpy as np
from os import listdir
from os.path import isfile,join
import utility as util
import math

if __name__ == '__main__':
    # If arguments were not provided in command line arguments,
    # prompt the user
    rootDir = util.safeGetDirectory()
    allFiles = [f for f in listdir(rootDir) if isfile(join(rootDir,f))]
    videoForProcessing = util.getVideoFile(allFiles)
    videoName = os.path.join(rootDir, videoForProcessing)
    x,y = util.getPixelRegion()
    encodingOption = util.getEncodingOption()

    print("Running PC " + encodingOption + " on " + videoForProcessing)

    video = cv2.VideoCapture(videoName)

    fileName = videoForProcessing.strip('.mp4') + "_" + encodingOption +".tpc"
    outputFile = open(fileName, 'w')

    frameNum = 0
    yFrameValues =np.ndarray
    t1= []
    t2= []
    t3= []
    t4= []
    count =0
    totalError = 0

    while(video.isOpened()):
        count += 1
        channels = 0
        ret,frame = video.read()
        if ret: #if video is still running...
            lastFrame = yFrameValues
            frameNum += 1

            croppedFrame = frame[x:x+10, y:y+10]
            yFrameValues = cv2.cvtColor(croppedFrame, cv2.COLOR_BGR2GRAY)

            if frameNum ==1:
                t4 = yFrameValues
                t3 = yFrameValues
                t2 = yFrameValues
                t1 = yFrameValues
            elif frameNum ==2:
                t4 = lastFrame
                t3 = lastFrame
                t2 = lastFrame
                t1 = lastFrame
            elif frameNum ==3:
                t4 = t1
                t3 = t1
                t2 = t1
                t1 = lastFrame
            elif frameNum ==4:
                t4 = t2
                t3 = t2
                t2 = t1
                t1 = lastFrame
            else:
                t4 = t3
                t3 = t2
                t2 = t1
                t1 = lastFrame


            if encodingOption == "1":
                writeToFile(outputFile, pc1(yFrameValues), frameNum)
            elif encodingOption == "2":
                if frameNum == 1:
                    outputFile.write("{\n" + str(yFrameValues) + "\n}\n")
                totalError += writeToFile(outputFile, pc2(yFrameValues,t1), frameNum)
            elif encodingOption == "3":
                if frameNum == 1 or frameNum == 2:
                    outputFile.write("{\n" + str(yFrameValues) + "\n}\n")
                totalError += writeToFile(outputFile, pc3(yFrameValues,t1,t2), frameNum)
            elif encodingOption == "4":
                if frameNum == 1 or frameNum == 2 or frameNum == 3 or frameNum == 4:
                    outputFile.write("{\n" + str(yFrameValues) + "\n}\n")
                totalError += writeToFile(outputFile, pc4(yFrameValues,t1,t2,t3,t4), frameNum)
        else:
            break

    if encodingOption == "1":
        print("No error since no predictive coding was done")
    else:
        print("Total error is: " + str(totalError))
