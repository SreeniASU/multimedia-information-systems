import cv2
import os.path
import numpy as np
from os import listdir
from os.path import isfile,join
import Utility as util
import math


def pc1 (yFrameValues):
return yFrameValues

def pc2(yFrameValues,t1):
    yFrameValues = yFrameValues.astype(float)
    result = np.zeros((10,10))
    print("Setting in initial value to ", yFrameValues[0,0])
    lastValue = t1#yFrameValues[0,0]

    for i in range(0,10):
        for j in range (0,10):
            result[i][j] = abs(yFrameValues[i,j] - lastValue)
            lastValue = yFrameValues[i,j]

    return result

def pc3(yFrameValues,t1,t2):
    yFrameValues = yFrameValues.astype(float)
    result = np.zeros((10,10))
    # print("Setting in initial values to ", yFrameValues[0,0], yFrameValues[0,1])

    for i in range(0,10):
        for j in range (0,10):
            previous_1 = t1#yFrameValues[util.goBack(i,j,1,10)]
            previous_2 = t2#yFrameValues[util.goBack(i,j,2,10)]
            predicted = (previous_1 + previous_2)/ 2
            result[i][j] = abs(yFrameValues[i,j] - predicted)

    return result

def pc4(yFrameValues,t1,t2,t3,t4):
    yFrameValues = yFrameValues.astype(float)
    result = np.zeros((10,10))
    # print("Setting in initial values to ", yFrameValues[0,0], yFrameValues[0,1])
    alpha1 = .5
    alpha2 = .5
    for i in range(0,10):
        for j in range (0,10):
            s1 = t1#yFrameValues[util.goBack(i,j,1,10)]
            s2 = t2#yFrameValues[util.goBack(i,j,2,10)]
            s3 = t3#yFrameValues[util.goBack(i,j,3,10)]
            s4 = t4#yFrameValues[util.goBack(i,j,4,10)]
            alpha2 = (s1 * s3 - s2**2)/(s3**2-s4*s2)
            alpha1 = 1.0- alpha2
            if alpha1 <0 or alpha1 >1 or math.isnan(alpha2):
            alpha1 = .5
            alpha2 = .5
            # print " set to .5"
            predicted = alpha1 * s1 + alpha2*s2
            # print(alpha1)
            result[i][j] = abs(yFrameValues[i,j] - predicted)
            # print result

    return result

def writeToFile(file, values,frameNum):
    rows = len(values)
    cols = len(values[0])
    for i in range(rows):
        for j in range(cols):
        contents = "< f" + str(frameNum) + ",(" + str(i) + "," + str(j) + "), " + str(values[i][j]) + " >\n"
        file.write(contents)

rootDir =os.path.join("E:","downloadsSSD","multimedia-information-systems-master","multimedia-information-systems-master","test","project1") # windows path
# rootDir = "/home/perry/Desktop/Project 2/multimedia-information-systems/Project 2/Part 1"#util.safeGetDirectory()
allFiles = [f for f in listdir(rootDir) if isfile(join(rootDir,f))]
videoForProcessing = "3.mp4" # util.getVideoFile(allFiles)
x,y = util.getPixelRegion()
encodingOption = "4"#util.getEncodingOption()

videoName = rootDir + "/" + videoForProcessing
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
while(video.isOpened()):
    count += 1
    channels = 0
    ret,frame = video.read()
    if ret: #if video is still running...
        frameNum += 1
        croppedFrame = frame[x:x+10, y:y+10]
        YCC_CroppedFrame = cv2.cvtColor(croppedFrame, cv2.COLOR_BGR2YCR_CB)


        if frameNum ==1:#t1 == []:
            yFrameValues = cv2.split(YCC_CroppedFrame)[0]
            t4 = yFrameValues
            t3 = yFrameValues
            t2 = yFrameValues
            t1 = yFrameValues

            # print "t1"
        elif frameNum ==2:#t2 == yFrameValues:
            # print "t2"
            yFrameValues = cv2.split(YCC_CroppedFrame)[0]
            t4 = yFrameValues
            t3 = yFrameValues
            t2 = t1
            t1 = yFrameValues
        elif frameNum ==3:#t3 == []:
            yFrameValues = cv2.split(YCC_CroppedFrame)[0]
            t4 = yFrameValues
            t3 = t2
            t2 = t1
            t1 = yFrameValues
        elif frameNum ==4:#t4 == []:
            yFrameValues = cv2.split(YCC_CroppedFrame)[0]
            t4 = t3
            t3 = t2
            t2 = t1
            t1 = yFrameValues

        else:
            t4 = t3
            t3 = t2
            t2 = t1
            t1 = yFrameValues
        yFrameValues = cv2.split(YCC_CroppedFrame)[0]


    '''
        if encodingOption == "1":
            writeToFile(outputFile, pc1(yFrameValues), frameNum)
        elif encodingOption == "2":
            writeToFile(outputFile, pc2(yFrameValues,t1), frameNum)
        elif encodingOption == "3":
            writeToFile(outputFile, pc3(yFrameValues,t1,t2), frameNum)
            #print pc3(yFrameValues)
        elif encodingOption == "4":
            # print pc4(yFrameValues)
            writeToFile(outputFile, pc4(yFrameValues,t1,t2,t3,t4), frameNum)
            #print yFrameValues





    else:
        break

'''
