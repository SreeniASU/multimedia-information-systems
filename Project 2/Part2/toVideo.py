__author__ = 'Team 6'

import cv2
import re
import sys
import numpy as np
from os import listdir
from os.path import dirname,join
import math

def uncodePC2(frames):
    result = np.empty_like(frames, dtype=np.uint8)
    for i in range(len(frames)):
        for x in range(0,10):
            for y in range (0,10):
                if y-1>=0:
                    result[i][x][y] = frames[i][x][y] + result[i][x][y-1]
                else:
                    result[i][x][y] = frames[i][x][y]

    return result

def uncodePC3(frames):
    result = np.empty_like(frames, dtype=np.uint8)
    for i in range(len(frames)):
        for x in range(0,10):
            for y in range (0,10):
                if x-1>=0:
                    result[i][x][y] = frames[i][x,y] + result[i][x-1,y]
                else:
                    result[i][x][y] = frames[i][x,y]

    return result

def uncodePC4(frames):
    result = np.empty_like(frames, dtype=np.uint8)
    for i in range(len(frames)):
        for x in range(10):
            for y in range(10):
                if x-1>=0 and y-1>=0:
                    result[i][x][y] = frames[i][x,y] + result[i][x-1,y-1]
                else:
                    result[i][x][y] = frames[i][x,y]

    return result

def uncodePC5(frames):
    result = np.empty_like(frames, dtype=np.float)
    for i in range(len(frames)):
        for x in range(10):
            for y in range(10):
                if x-1>=0 and y-1>=0:
                    result[i][x][y] = frames[i][x,y] + ( result[i][x-1,y-1]/float(3) +  result[i][x-1,y]/float(3) +  result[i][x,y-1]/float(3))
                elif x-1>=0:
                    result[i][x][y] = frames[i][x,y] + result[i][x-1,y]
                elif y-1>=0:
                    result[i][x][y] = frames[i][x,y] + result[i][x,y-1]
                else:
                    result[i][x][y] = frames[i][x,y]

    return np.array(result, dtype=np.uint8)

def parseFile(filepath):
    inputFile = open(filepath, 'r')
    frames = []
    frame = -1
    for line in inputFile.readlines():
        result = re.match("< f(?P<f>\d+),\((?P<x>\d),(?P<y>\d)\), (?P<e>-?\d+(.*)?) >\n", line)
        if result:
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
    
    return np.array(frames)


if __name__ == '__main__':
    filepath = join(dirname(__file__), sys.argv[1])
    option = int((sys.argv[1].split('_',1)[1]).strip(".spc")) #gets number from filename
    print("Using decoding option" + str(option))

    frames = parseFile(filepath)

    if option == 1:
        result = np.array(frames, dtype=np.uint8)
    elif option == 2:
        result = uncodePC2(frames)
    elif option == 3:
        result = uncodePC3(frames)
    elif option == 4:
        result = uncodePC4(frames)
    elif option == 5:
        result = uncodePC5(frames)
    else:
        print("Unknown option " + str(option))

    tempVideo = cv2.VideoWriter(sys.argv[1].strip(".tpc") + ".avi", cv2.cv.CV_FOURCC('m', 'p', '4', 'v'), 29.41176470588235, (10, 10), False)
    for frame in result:
        betterResult = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        tempVideo.write(betterResult)
