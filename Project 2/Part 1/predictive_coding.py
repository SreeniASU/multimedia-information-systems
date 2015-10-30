__author__ = "Team 6"

import cv2
import os.path
import sys
import numpy as np
from os import listdir
from os.path import isfile,join
import utility as util
import math


def pc1 (yFrameValues):
    return yFrameValues

def pc2(yFrameValues,t1):
    yFrameValues = yFrameValues.astype(float)
    result = np.zeros((10,10))
    #print("Setting in initial value to ", yFrameValues[0,0])

    for i in range(0,10):
        for j in range (0,10):
            #print("yFrameValues[" + str(i) + "][" + str(j) + "]: " + str(yFrameValues[i][j]))
            #print("t1[" + str(i) + "][" + str(j) + "]: " + str(t1[i][j]))
            result[i][j] = yFrameValues[i][j] - t1[i][j]

    return result

def pc3(yFrameValues,t1,t2):
    yFrameValues = yFrameValues.astype(float)
    result = np.zeros((10,10))
    # print("Setting in initial values to ", yFrameValues[0,0], yFrameValues[0,1])

    for i in range(0,10):
        for j in range (0,10):
            previous_1 = float(t1[i][j])#yFrameValues[util.goBack(i,j,1,10)]
            previous_2 = float(t2[i][j])#yFrameValues[util.goBack(i,j,2,10)]
            predicted = (previous_1 + previous_2)/ 2
            result[i][j] = yFrameValues[i][j] - predicted

    return result

def pc4(yFrameValues,t1,t2,t3,t4):
    yFrameValues = yFrameValues.astype(float)
    result = np.zeros((10,10))
    # print("Setting in initial values to ", yFrameValues[0,0], yFrameValues[0,1])
    alpha1 = .5
    alpha2 = .5
    for i in range(0,10):
        for j in range (0,10):
            s1 = float(t1[i,j])#yFrameValues[util.goBack(i,j,1,10)]
            s2 = float(t2[i,j])#yFrameValues[util.goBack(i,j,2,10)]
            s3 = float(t3[i,j])#yFrameValues[util.goBack(i,j,3,10)]
            s4 = float(t4[i,j])#yFrameValues[util.goBack(i,j,4,10)]
            print("s1:", s1)
            print("s2:", s2)
            print("s3:", s3)
            print("s4:", s4)
            try:
                alpha2 = (s1 * s3 - s2**2)/(s3**2-s4*s2)
            except:
                alpha2 = 0.5
                pass
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

def writeToFile(file, values,frameNum,initialValue=False,initialValue2=False):
    rows = len(values)
    cols = len(values[0])
    frameError = 0

    if (initialValue2 and initialValue):
        # file.write(str("{" + initialValue + "," + intialValue2 + "}") + "\n")
        file.write("{" + str(initialValue) + "," + str(initialValue2) + "}" + "\n")
    elif (initialValue):
        # file.write(str("{" + initialValue + "}") + "\n")
        file.write("{" + str(initialValue) + "}" + "\n")
    for i in range(rows):
        for j in range(cols):
            contents = "< f" + str(frameNum) + ",(" + str(i) + "," + str(j) + "), " + str(values[i][j]) + " >\n"
            frameError += abs(values[i][j])
            file.write(contents)

    return frameError

if __name__ == '__main__':
    if (len(sys.argv) == 1):
        rootDir = rootDir or util.safeGetDirectory()
        allFiles = [f for f in listdir(rootDir) if isfile(join(rootDir,f))]
        videoForProcessing = util.getVideoFile(allFiles)
        videoName = rootDir + "/" + videoForProcessing
        x,y = util.getPixelRegion()
        encodingOption = util.getEncodingOption()
    elif (len(sys.argv) == 5):
        videoForProcessing = os.path.basename(sys.argv[1])
        videoName = os.path.join(os.path.dirname(__file__), sys.argv[1])
        x = int(sys.argv[2])
        y = int(sys.argv[3])
        encodingOption = sys.argv[4]
    else:
        print("error: must have either 0 arguments or 5 arguments of the form\npython predictive_coding.py file x y p\n")


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
                temp = yFrameValues
                yFrameValues = cv2.split(YCC_CroppedFrame)[0]
                t4 = yFrameValues
                t3 = yFrameValues
                t2 = temp
                t1 = temp
            elif frameNum ==3:#t3 == []:
                temp = yFrameValues
                yFrameValues = cv2.split(YCC_CroppedFrame)[0]
                t4 = yFrameValues
                t3 = t2
                t2 = t1
                t1 = yFrameValues
            elif frameNum ==4:#t4 == []:
                t4 = t3
                t3 = t2
                t2 = t1
                t1 = yFrameValues
                yFrameValues = cv2.split(YCC_CroppedFrame)[0]
            else:
                t4 = t3
                t3 = t2
                t2 = t1
                t1 = yFrameValues
                yFrameValues = cv2.split(YCC_CroppedFrame)[0]


            if encodingOption == "1":
                writeToFile(outputFile, pc1(yFrameValues), frameNum)
            elif encodingOption == "2":
                if frameNum == 1:
                    outputFile.write("{" + str(yFrameValues) + "}\n")
                print("yFrameValues:", yFrameValues)
                print("t1:", t1)
                totalError += writeToFile(outputFile, pc2(yFrameValues,t1), frameNum)
            elif encodingOption == "3":
                if frameNum == 1 or frameNum == 2:
                    outputFile.write("{" + str(yFrameValues) + "}\n")
                totalError += writeToFile(outputFile, pc3(yFrameValues,t1,t2), frameNum)
                #print pc3(yFrameValues)
            elif encodingOption == "4":
                #print pc4(yFrameValues)
                if frameNum == 1 or frameNum == 2 or frameNum == 3 or frameNum == 4:
                    outputFile.write("{" + str(yFrameValues) + "}\n")
                totalError += writeToFile(outputFile, pc4(yFrameValues,t1,t2,t3,t4), frameNum)
                #print yFrameValues
        else:
            break

    if encodingOption == "1":
        print("No error since no predictive coding was done")
    else:
        print("Total error is:" + str(totalError))
