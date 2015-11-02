__author__ = 'Team 6'

import cv2
import sys
import os.path
import utility as util
from tpcToVideo import tpcToVideo
from spcToVideo import spcToVideo

if __name__ == '__main__':
    path = sys.argv[1]
    filepath = os.path.join(os.path.dirname(__file__), path)
    option = int(os.path.basename(path).split('.', 1)[0].split('_',2)[1]) #gets number from filename
    ext = os.path.basename(path).split('.', 1)[1]
    print("Using decoding option" + str(option))

    initials, frames = util.parseFile(filepath)

    if ext == 'spq':
        result = spcToVideo(frames, option)
    elif ext == 'tpq':
        result = tpcToVideo(initials, frames, option)

    print(result)

    tempVideo = cv2.VideoWriter(os.path.basename(path).split('.', 1)[0] + ".avi", cv2.cv.CV_FOURCC('m', 'p', '4', 'v'), 29.41176470588235, (10, 10), False)
    for frame in result:
        rgbResult = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        tempVideo.write(rgbResult)
