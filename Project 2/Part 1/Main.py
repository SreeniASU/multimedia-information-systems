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
            result[i][j] = yFrameValues[i,j] - lastValue
            lastValue = yFrameValues[i,j]

    return result

def pc3(frameT1, frameT2, frameCur,init):

    frameT1 = frameT1.astype(float)
    result = np.zeros((10,10))
    if init: #need a special case for getting the errors for the second frame
        for i in range(0,10):
            for j in range (0,10):
                result[i][j] = frameCur[i,j] - frameT1[i,j]
    else:
        frameT2 = frameT2.astype(float)
        frameCur = frameCur.astype(float)

        #print("Setting in initial values to ", yFrameValues[0,0], yFrameValues[0,1])

        for i in range(0,10):
            for j in range (0,10):
                previous_1 = frameT1[i,j]
                previous_2 = frameT2[i,j]
                predicted = (previous_1 + previous_2)/ 2
                result[i][j] = frameCur[i,j] - predicted

    return result

def pc4(yFrameValues):
    yFrameValues = yFrameValues.astype(float)
    result = np.zeros((10,10))
    print("Setting in initial values to ", yFrameValues[0,0], yFrameValues[0,1])
    alpha1 = .5
    alpha2 = .5
    for i in range(0,10):
        for j in range (0,10):
            s1 = yFrameValues[util.goBack(i,j,1,10)]
            s2 = yFrameValues[util.goBack(i,j,2,10)]
            s3 = yFrameValues[util.goBack(i,j,3,10)]
            s4 = yFrameValues[util.goBack(i,j,4,10)]
            # predicted = (previous_1 + previous_2)/ 2
            alpha2 = (s1 * s3 - s2^2)/(s3^2-s4*s2)
            alpha1 = 1.0- alpha2
            result[i][j] = yFrameValues[i,j] - predicted
            print result

    return result

def writeToFile(file, values,frameNum,initialValue,initialValue2):
    rows = len(values)
    cols = len(values[0])

    if (initialValue2):
        # file.write(str("{" + initialValue + "," + intialValue2 + "}") + "\n")
        file.write("{" + str(initialValue) + "," + str(initialValue2) + "}" + "\n")
    else:
        # file.write(str("{" + initialValue + "}") + "\n")
        file.write("{" + str(initialValue) + "}" + "\n")


    for i in range(rows):
        for j in range(cols):
            contents = "< f" + str(frameNum) + ",(" + str(i) + "," + str(j) + "), " + str(values[i][j]) + " >\n"
            file.write(contents)
rootDir = "/home/perry/Desktop/CSE408/multimedia-information-systems/test/project1"#util.safeGetDirectory()
#rootDir = util.safeGetDirectory()
allFiles = [f for f in listdir(rootDir) if isfile(join(rootDir,f))]
videoForProcessing = "3.mp4"#util.getVideoFile(allFiles)
x,y = (3,4)#util.getPixelRegion()
encodingOption = '3' #util.getEncodingOption()

videoName = rootDir + "/" + videoForProcessing
video = cv2.VideoCapture(videoName)

fileName = videoForProcessing.strip('.mp4') + "_" + encodingOption +".tpc"
outputFile = open(fileName, 'w')
frameNum = 0
frame1 = []
frame2 = []
frame3 = []
frame4 = []
while(video.isOpened()):
    channels = 0
    ret,frame = video.read()
    if ret: #if video is still running...
        frameNum += 1
        croppedFrame = frame[x:x+10, y:y+10]
        YCC_CroppedFrame = cv2.cvtColor(croppedFrame, cv2.COLOR_BGR2YCR_CB)
        yFrameValues = cv2.split(YCC_CroppedFrame)[0]
        if encodingOption == "3":
            if frameNum == 1:
                frame1 = yFrameValues
                print("Getting frame 1: " + str(frame1[0,0]) + "\n")
                #writeToFile(outputFile,frame1,) writing to file still needs to be done to preserve values
                continue
            elif frameNum == 2:
                frame2 = pc3(frame1,None,yFrameValues,True)
                print("Getting frame 2: " + str(frame2[0,0]) + "\n")
                #write to file
                continue
            else:
                frame3 = pc3(frame1,frame2,yFrameValues,False)
                print("Getting frame " + str(frameNum) +  ":" + str(frame3[0,0]) + "\n")
                print("Swapping frames around\n")
                #write to file
                frame1 = frame2
                frame2 = frame3
                continue



           # writeToFile(outputFile, pc3(yFrameValues), frameNum,yFrameValues[0,0],yFrameValues[0,1])
            #print pc3(yFrameValues)



    '''
        if encodingOption == "1":
            writeToFile(outputFile, pc1(yFrameValues), frameNum,yFrameValues[0,0])
        elif encodingOption == "2":
            writeToFile(outputFile, pc2(yFrameValues), frameNum,yFrameValues[0,0])
        elif encodingOption == "4":
            print pc4(yFrameValues)
            writeToFile(outputFile, pc4(yFrameValues), frameNum,yFrameValues[0,0])
    else:
        break
'''