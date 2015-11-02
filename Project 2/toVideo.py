__author__ = 'Team 6'

import cv2
import sys
from os import listdir
import os.path
from os.path import isfile,join
import Part5.utility as util
from Part4.Main import LZWDecode,shannonFanoDecode
from Part5.tpcToVideo import tpcToVideo
from Part5.spcToVideo import spcToVideo

if __name__ == '__main__':

    rootDir = util.safeGetDirectory()
    allFiles = [f for f in listdir(rootDir) if isfile(join(rootDir,f))]
    inputFileName =  util.getVideoFile(allFiles)
    filepath = os.path.join(rootDir, inputFileName)
    coding_option = int(os.path.basename(inputFileName).split('.', 1)[0].split('_',2)[1]) #gets number from filename
    ext = os.path.basename(inputFileName).split('.', 1)[1]

    if ext == 'spv' or ext == 'tpv':
        compression_option = int(os.path.basename(inputFileName).split('.', 1)[0].split('_',3)[3])
        if compression_option == 1:
            filepath = filepath
        elif compression_option == 2:
            print (filepath)
            filepath = shannonFanoDecode(filepath)
        elif compression_option == 3:
            print (filepath)
            filepath = LZWDecode(filepath)
        elif compression_option == 4:
            print(filepath)
            # filepath = arithmeticDecode(frames)
        else:
            print("Unknown compression option " + str(compression_option))

    initials, frames = util.parseFile(filepath)

    if ext == 'spq' or ext == 'spc' or ext == 'spv':
        result = spcToVideo(frames, coding_option)
    elif ext == 'tpq' or ext == 'tpc' or ext == 'tpv':
        print(filepath)
        result = tpcToVideo(initials, frames, coding_option)
    else:
        print("Unknown extension " + str(ext))

    tempVideo = cv2.VideoWriter(os.path.basename(inputFileName).split('.', 1)[0] + ".avi", cv2.cv.CV_FOURCC('m', 'p', '4', 'v'), 29.41176470588235, (10, 10), False)
    for frame in result:
        rgbResult = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        tempVideo.write(rgbResult)
