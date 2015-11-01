__author__ = 'Team 6'

import cv2
import sys
import os.path
import numpy as np
from os import listdir
import utility as util
import math

def uncodeSPC2(frames):
    result = np.empty_like(frames, dtype=np.uint8)
    for i in range(len(frames)):
        for x in range(0,10):
            for y in range (0,10):
                if y-1>=0:
                    result[i][x][y] = frames[i][x][y] + result[i][x][y-1]
                else:
                    result[i][x][y] = frames[i][x][y]

    return result

def uncodeSPC3(frames):
    result = np.empty_like(frames, dtype=np.uint8)
    for i in range(len(frames)):
        for x in range(0,10):
            for y in range (0,10):
                if x-1>=0:
                    result[i][x][y] = frames[i][x,y] + result[i][x-1,y]
                else:
                    result[i][x][y] = frames[i][x,y]

    return result

def uncodeSPC4(frames):
    result = np.empty_like(frames, dtype=np.uint8)
    for i in range(len(frames)):
        for x in range(10):
            for y in range(10):
                if x-1>=0 and y-1>=0:
                    result[i][x][y] = frames[i][x,y] + result[i][x-1,y-1]
                else:
                    result[i][x][y] = frames[i][x,y]

    return result

def uncodeSPC5(frames):
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

def spcToVideo(frames, option):
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

    return result

if __name__ == '__main__':
    path = sys.argv[1]
    filepath = os.path.join(os.path.dirname(__file__), path)
    option = int(os.path.basename(path).split('.', 1)[0].split('_',1)[1]) #gets number from filename
    print("Using decoding option" + str(option))

    _, frames = util.parseFile(filepath)

    result = spcToVideo(frames, option)

    tempVideo = cv2.VideoWriter(os.path.basename(path).split('.', 1)[0] + ".avi", cv2.cv.CV_FOURCC('m', 'p', '4', 'v'), 29.41176470588235, (10, 10), False)
    for frame in result:
        rgbResult = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        tempVideo.write(rgbResult)
