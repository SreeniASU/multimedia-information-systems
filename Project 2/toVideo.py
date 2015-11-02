__author__ = 'Team 6'

import cv2
import sys
import os.path
import Part5.utility as util
from Part5.tpcToVideo import tpcToVideo
from Part5.spcToVideo import spcToVideo
'''
from Part4.Main import *
from Part4.lzw import decodeLZW
from Part4.lzw import decodeLZW
from Part4.lzw import decodeLZW
'''

if __name__ == '__main__':
    path = sys.argv[1]
    filepath = os.path.join(os.path.dirname(__file__), path)
    coding_option = int(os.path.basename(path).split('.', 1)[0].split('_',2)[1]) #gets number from filename
    ext = os.path.basename(path).split('.', 1)[1]

    if ext == 'spv' or ext == 'tpv':
        compression_option = int(os.path.basename(path).split('.', 1)[0].split('_',3)[3])
        if compression_option == 1:
            filepath = filepath
        elif compression_option == 2:
            filepath = decodeShannonFano(filepath)
        elif compression_option == 3:
            filepath = decodeLZW(filepath)
        elif compression_option == 4:
            filepath = decodeArithmetic(frames)
        else:
            print("Unknown compression option " + str(compression_option))

    initials, frames = util.parseFile(filepath)

    if ext == 'spq' or ext == 'spc' or ext == 'spv':
        result = spcToVideo(frames, coding_option)
    elif ext == 'tpq' or ext == 'tpc' or ext == 'tpv':
        result = tpcToVideo(initials, frames, coding_option)
    else:
        print("Unknown extension " + str(ext))

    tempVideo = cv2.VideoWriter(os.path.basename(path).split('.', 1)[0] + ".avi", cv2.cv.CV_FOURCC('m', 'p', '4', 'v'), 29.41176470588235, (10, 10), False)
    for frame in result:
        rgbResult = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        tempVideo.write(rgbResult)
