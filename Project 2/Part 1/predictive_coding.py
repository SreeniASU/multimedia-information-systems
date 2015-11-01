__author__ = "Team 6"

import cv2
import os.path
import sys
import numpy as np
from os import listdir
from os.path import isfile,join
import utility as util
import math

# For option 1, we perform no predictive coding, simply
# Setting the coded pixel values as the error values. There
# is no need to log initial values.
def pc1 (yFrameValues):
    return yFrameValues

# For option 2, we use the value of the pixel from the previous
# frame as the predictor for the current pixel. The first frame should
# be printed at the top of the file and after that all of the error
# values
def pc2(yFrameValues,t1):
    yFrameValues = yFrameValues.astype(float)
    result = np.zeros((10,10))

    for i in range(0,10):
        for j in range (0,10):
            result[i][j] = yFrameValues[i][j] - t1[i][j]

    return result

# For option 3, two of the previous frame values are used, and an
# average of the pixel value in those frames is used for the predictor
# of the pixel value in this frame
def pc3(yFrameValues,t1,t2):
    yFrameValues = yFrameValues.astype(float)
    result = np.zeros((10,10))

    for i in range(0,10):
        for j in range (0,10):
            previous_1 = float(t1[i][j])
            previous_2 = float(t2[i][j])
            predicted = (previous_1 + previous_2)/ 2
            result[i][j] = yFrameValues[i][j] - predicted

    return result

# Using the predictor described in the assignement, a waited
# average of the past two values is used that creates a more
# optimal predictor
def pc4(yFrameValues,t1,t2,t3,t4):
    yFrameValues = yFrameValues.astype(float)
    result = np.zeros((10,10))
    alpha1 = .5
    alpha2 = .5
    for i in range(0,10):
        for j in range (0,10):
            s1 = float(t1[i][j])
            s2 = float(t2[i][j])
            s3 = float(t3[i][j])
            s4 = float(t4[i][j])
            try:
                if s3**2 - s4*s2 == 0:
                    alpha2 = 0.5
                else:
                    alpha2 = (s1 * s3 - s2**2)/(s3**2-s4*s2)
            except:
                alpha2 = 0.5
                pass

            if alpha2 < 0 or alpha2 > 1 or math.isnan(alpha2):
                alpha2 = .5

            alpha1 = 1 - alpha2

            predicted = alpha1 * s1 + alpha2*s2
            result[i][j] = (yFrameValues[i][j] - predicted)

    return result

def writeToFile(file, values,frameNum):
    rows = len(values)
    cols = len(values[0])
    frameError = 0

    for i in range(rows):
        for j in range(cols):
            contents = "< f" + str(frameNum) + ",(" + str(i) + "," + str(j) + "), " + str(values[i][j]) + " >\n"
            frameError += abs(values[i][j])
            file.write(contents)

    return frameError

if __name__ == '__main__':
    # If arguments were not provided in command line arguments,
    # prompt the user
    if (len(sys.argv) == 1):
        rootDir = util.safeGetDirectory()
        allFiles = [f for f in listdir(rootDir) if isfile(join(rootDir,f))]
        videoForProcessing = util.getVideoFile(allFiles)
        videoName = os.path.join(rootDir, videoForProcessing)
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

    print("Running PC " + encodingOption + " on " + videoForProcessing)

    video = cv2.VideoCapture(videoName)

    fileName = videoForProcessing.strip('.mp4') + "_" + encodingOption +".tpc"
    outputFile = open(fileName, 'w')

    # Output a temp black and white video to compare against part 5
    tempVideo = cv2.VideoWriter(videoForProcessing.strip('.mp4') + ".avi", cv2.cv.CV_FOURCC('m', 'p', '4', 'v'), video.get(cv2.cv.CV_CAP_PROP_FPS), (10, 10), False)

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
            tempVideo.write(cv2.cvtColor(yFrameValues, cv2.COLOR_GRAY2BGR))

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
