__author__ = 'Team 6'

import cv2
import re
import sys
import os.path
import numpy as np
from os import listdir
from os.path import isfile,join
import utility as util
import math

# Utility function for converting initialization string to
# a matrix
def stringToMatrix(matrixString):
    lines = matrixString.strip().split('\n')
    result = []
    for line in lines:
        values = line.strip(' []').split(' ')
        i = 0
        while i < len(values):
            if (len(values[i]) == 0):
                values.pop(i)
            else:
                values[i] = int(values[i])
                i += 1

        result.append(values)

    return result

def uncodePC2(initials, frames):
    result = np.empty_like(frames, dtype=np.uint8)
    lastFrame = np.array(initials[0], dtype=np.uint8)
    for i in range(len(frames)):
       result[i] = np.add(lastFrame, frames[i])
       lastFrame = result[i]

    return result

def uncodePC3(initials, frames):
    result = np.empty_like(frames, dtype=np.float)
    result[0] = initials[0]
    result[1] = initials[1]
    for i in range(2, len(frames)):
        predictor = np.empty_like(frames[i], dtype=np.float)
        predictor = np.add(result[i-1], result[i-2]) / 2
        result[i] = np.add(frames[i], predictor)
    return np.array(result, dtype=np.uint8)

def uncodePC4(initials, frames):
    result = np.empty_like(frames, dtype=np.float)
    result[0] = initials[0]
    result[1] = initials[1]
    result[2] = initials[2]
    result[3] = initials[3]
    for i in range(4, len(frames)):
        predictor = np.empty_like(frames[i], dtype=np.float)

        try:
            alpha2 = float((result[i-1] * result[i-3] - result[i-2]**2)/(result[i-3]**2-result[i-4]*result[i-2]))
        except:
            alpha2 = 0.5
            pass
        if alpha2 < 0 or alpha2 > 1 or math.isnan(alpha2):
            alpha2 = .5

        alpha1 = 1 - alpha2

        predictor = np.add(alpha1 * result[i-1], alpha2 * result[i-2])
        print(predictor)
        result[i] = np.add(frames[i], predictor)
    return np.array(result, dtype=np.uint8)

def parseFile(filepath):
    inputFile = open(filepath, 'r')
    frames = []
    initString = ""
    init = []
    initFlag = False
    frame = -1
    for line in inputFile.readlines():
        if line[0] == "{":
            initFlag = True
        elif initFlag :
            if line[0]== "}": #finds end of initial value
               initFlag = False
               init.append(stringToMatrix(initString))
               initString = ""
            else:
               initString += line     # adds all lines of initial value of a frame to init.
        else:
            result = re.match("< f(?P<f>\d+),\((?P<x>\d),(?P<y>\d)\), (?P<e>-?\d+(.*)?) >\n", line)
            f = int(result.group("f")) - 1
            x = int(result.group("x"))
            y = int(result.group("y"))
            if (re.match(".*e.*",result.group("e"))):
                e = 0
            else:
                e = float(result.group("e"))

            if (f > frame):
                frames.append(np.empty([10,10]))
                frame += 1
            
            frames[f][x][y] = e
    
    return init, np.array(frames)


if __name__ == '__main__':
    # rootDir =os.path.join("E:","downloadsSSD","multimedia-information-systems-master")#,"multimedia-information-systems-master","test","project1") # windows path
    filepath = os.path.join(os.path.dirname(__file__), sys.argv[1])
    option = int((sys.argv[1].split('_',1)[1]).strip(".tpc")) #gets number from filename
    print(option)

    initials, frames = parseFile(filepath)

    if option == 1:
        result = np.array(frames, dtype=np.uint8)
    elif option == 2:
        result = uncodePC2(initials, frames)
    elif option == 3:
        result = uncodePC3(initials, frames)
    else:
        result = uncodePC4(initials, frames)

    tempVideo = cv2.VideoWriter(sys.argv[1].strip(".tpc") + ".avi", cv2.cv.CV_FOURCC('m', 'p', '4', 'v'), 29.41176470588235, (10, 10), False)
    print(initials[0])
    print(initials[1])
    print(result[2])
    for frame in result:
        betterResult = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        tempVideo.write(betterResult)
