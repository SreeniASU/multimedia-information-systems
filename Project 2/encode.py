__author__ = "Team 6"

import cv2
import os.path
import sys
import numpy as np
from os import listdir
from os.path import isfile,join
import Part1.Main as tpc
import Part2.Main as spc
import Part3.Main as quant
import Part4.Main as comp
import Part1.Utility as tpcUtil
import Part2.Utility as spcUtil
import Part4.Utility as cmpUtil
import math

def getCoding():
    while 1:
        try:
            option = input("Which predictive coding do you want to use?\n" +
                         "1: Temporal coding\n" +
                         "2: Spatial coding\n> ")
            if option > 2 or option < 1:
                print(str(option) + " is not a valid selection. Please make a different selection.\n")
            else:
                print("Option: " + str(math.floor(option)) + " selected.")
                return math.floor(option)
        except:
            print(str(option) + " is not a valid input. Please try again.\n")

if __name__ == '__main__':
    # If arguments were not provided in command line arguments,
    # prompt the user
    rootDir = tpcUtil.safeGetDirectory()
    allFiles = [f for f in listdir(rootDir) if isfile(join(rootDir,f))]
    videoForProcessing = tpcUtil.getVideoFile(allFiles)
    videoName = os.path.join(rootDir, videoForProcessing)
    print("Reading video file...")
    video = cv2.VideoCapture(videoName)
    x,y = tpcUtil.getPixelRegion()
    coding = getCoding()

    if coding == 1:
        encodingOption = tpcUtil.getEncodingOption()
        pcFileName = videoName.strip('.mp4') + "_" + encodingOption +".tpc"
        outputFile = open(pcFileName, 'w')
        tpc.temporalCoding(video, x, y, encodingOption, outputFile)
    elif coding == 2:
        encodingOption = spcUtil.getEncodingOption()
        pcFileName = videoName.strip('.mp4') + "_" + encodingOption +".spc"
        outputFile = open(pcFileName, 'w')
        spc.spatialCoding(video, x, y, encodingOption, outputFile)

    print("Coded file saved to " + pcFileName)

    quantizeOption = quant.getOption()
    quantizeFileName = quant.quantize(pcFileName, quantizeOption)
    print("Quantized file saved to " + quantizeFileName)

    compressionOption = cmpUtil.selectCodingOption()
    compressionFileName = comp.compress(quantizeFileName, compressionOption, rootDir)
