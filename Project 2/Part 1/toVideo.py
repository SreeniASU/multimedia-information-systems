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
    return frames

def uncodePC4(initials, frames):
    return frames

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
            else:
               initString += line     # adds all lines of initial value of a frame to init.
        else:
            result = re.match("< f(?P<f>\d+),\((?P<x>\d),(?P<y>\d)\), (?P<e>-?\d+(.\d*)?) >\n", line)
            f = int(result.group("f")) - 1
            x = int(result.group("x"))
            y = int(result.group("y"))
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
    for frame in result:
        betterResult = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        tempVideo.write(betterResult)
#
# flags = ""
#
# for f in frames:
#     image = cv2.imdecode(f, flags)
#
#
#     cv2.WriteFrame(writer, image)
