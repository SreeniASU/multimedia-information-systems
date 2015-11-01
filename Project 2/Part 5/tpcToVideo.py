__author__ = 'Team 6'

import cv2
import sys
import os.path
import numpy as np
from os import listdir
import utility as util
import math

def uncodeTPC2(initials, frames):
    result = np.empty_like(frames, dtype=np.uint8)
    lastFrame = np.array(initials[0], dtype=np.uint8)
    for i in range(len(frames)):
       result[i] = np.add(lastFrame, frames[i])
       lastFrame = result[i]

    return result

def uncodeTPC3(initials, frames):
    result = np.empty_like(frames, dtype=np.float)
    result[0] = initials[0]
    result[1] = initials[1]
    for i in range(2, len(frames)):
        predictor = np.empty_like(frames[i], dtype=np.float)
        predictor = np.add(result[i-1], result[i-2]) / 2
        result[i] = np.add(frames[i], predictor)
    return np.array(result, dtype=np.uint8)

def uncodeTPC4(initials, frames):
    result = np.empty_like(frames, dtype=np.float)
    result[0] = initials[0]
    result[1] = initials[1]
    result[2] = initials[2]
    result[3] = initials[3]
    for i in range(4, len(frames)):
        predictor = np.empty_like(frames[i], dtype=np.float)

        for x in range(10):
            for y in range(10):
                s1 = result[i-1][x][y]
                s2 = result[i-2][x][y]
                s3 = result[i-3][x][y]
                s4 = result[i-4][x][y]

                try:
                    if s3**2-s4*s2 == 0:
                        alpha2 = 0.5
                    else:
                        alpha2 = (s1 * s3 - s2**2)/(s3**2-s4*s2)
                except Exeption, x:
                    alpha2 = 0.5
                    pass

                if alpha2 < -0.000001 or alpha2 > 1.000001 or math.isnan(alpha2):
                    alpha2 = .5

                alpha1 = 1 - alpha2

                predictor = alpha1 * result[i-1][x][y] + alpha2 * result[i-2][x][y]
                result[i][x][y] = frames[i][x][y] + predictor

        print(result[i])

    return np.array(result, dtype=np.uint8)

def tpcToVideo(initials, frames, option):
    if option == 1:
        result = np.array(frames, dtype=np.uint8)
    elif option == 2:
        result = uncodeTPC2(initials, frames)
    elif option == 3:
        result = uncodeTPC3(initials, frames)
    else:
        result = uncodeTPC4(initials, frames)

    return result

if __name__ == '__main__':
    path = sys.argv[1]
    filepath = os.path.join(os.path.dirname(__file__), path)
    option = int(os.path.basename(path).split('.', 1)[0].split('_',1)[1]) #gets number from filename
    print("Using decoding option" + str(option))

    initials, frames = util.parseFile(filepath)

    result = tpcToVideo(initials, frames, option)

    tempVideo = cv2.VideoWriter(os.path.basename(path).split('.', 1)[0] + ".avi", cv2.cv.CV_FOURCC('m', 'p', '4', 'v'), 29.41176470588235, (10, 10), False)
    for frame in result:
        rgbResult = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        tempVideo.write(rgbResult)
