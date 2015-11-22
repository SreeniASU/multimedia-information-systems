import sys
import math
import numpy as np
import cv2
import matplotlib.pyplot as plt
import re
import Utility as util
from os import listdir,path

'''
Quantizes a block using the number of bins
Returns a formatted string for output to a file which details the information in the format:
< FrameNumber, (X coordinate, Y coordinate) , Y Channel Value, Number Of Occurances >
'''
def quantizeBlock(block, bins, frameNum, x, y):
    minValue = np.amin(block)
    maxValue = np.amax(block)
    samples, valuesPerBin = np.linspace(minValue, maxValue, bins, endpoint=False, retstep=True)
    samples += 0.5*valuesPerBin
    samples = map((lambda v: round(v, 7)), samples)
    occurancesInFrame = dict.fromkeys(samples, 0) #dictionary to contain how many times a value occurs

    for val in np.nditer(block):
        if valuesPerBin == 0:
            bottomBin = minValue
        else:
            bottomBin = minValue + (math.floor((val - minValue) / valuesPerBin) + 0.5) * valuesPerBin

        if bottomBin >= maxValue:
            bottomBin = minValue + (bins - 0.5)*valuesPerBin

        bottomBin = round(bottomBin, 7)
        occurancesInFrame[bottomBin] += 1

    result = list()

    for key in occurancesInFrame:
        result.append({
            'frameNum': frameNum,
            'blockCoords': (x, y),
            'key': key,
            'val': occurancesInFrame[key]
        })

    return result

def quantize(frameData, n):
    print('Running quantization with ' + str(n) + ' bins...')

    result = list()
    frameNum = 0

    #for each entry in frameData
    for frame in frameData:
        frameNum += 1
        print('Processing regions of frame: ' + str(frameNum))
        for blockI in range(0, len(frame), 8):
            for blockJ in range(0, len(frame[blockI]), 8):
                block = frame[blockI:blockI+8,blockJ:blockJ+8]
                result.extend(quantizeBlock(block, n, frameNum, blockI, blockJ))

    return result

def writeHistogramToFile(quantizedFrameBlocks, fileName):
    outputFile = open(fileName, 'w')
    for item in quantizedFrameBlocks:
        outputFile.write('< ' + str(item['frameNum']) + ', ' + str(item['blockCoords']) + ', ' + str(item['key']) + ', ' + str(item['val']) + ' >\n')
    outputFile.close()

def displayHistogram(quantizedFrameBlocks, n, fromFile=False, imageFile=''):
    print('Creating histogram.')
    histDict = dict()

    if fromFile:
        quantizedFrameBlocks = readFile(quantizedFrameBlocks)

    for item in quantizedFrameBlocks:
        if item['key'] not in histDict:
            histDict[item['key']] = 0

        histDict[item['key']] += item['val']  #increment the value at the key by the given

    plt.hist(histDict.keys(), bins=n, weights=histDict.values()) #need to add bars maybe? not sure here

    if len(imageFile) > 0:
        print 'Saving histogram image to ' + imageFile
        plt.savefig(imageFile)

    print('Press any key or click to continue.')
    plt.show()


'''
Main Method
Prompts the user for an input file, a quantization option selection, and an m value.
Uses these values to quantize the input files error into 2^m uniform bins.
'''
if __name__ == '__main__':
    if len(sys.argv) == 1:
        rootDir = util.safeGetDirectory()
        allFiles = [f for f in listdir(rootDir) if isfile(join(rootDir,f))]
        input_file = util.getVideoFile(allFiles)
        n = util.getNValue()
        fileName = path.join(rootDir,input_file)
    elif len(sys.argv) == 3:
        fileName = path.realpath(sys.argv[2])
        n = int(sys.argv[1])
    else:
        print 'Usage: python block_quantize.py 6 ../path/to/file.mp4'
        exit()


    # Read video data
    video = cv2.VideoCapture(fileName)
    frameData = util.getContent(video)

    # Quantize the blocks of the video
    quantizedBlocks = quantize(frameData, n)

    # Write the data to the file
    outputFileName = fileName.replace('.mp4','_hist_' + str(n) + '.hst') 
    writeHistogramToFile(quantizedBlocks, outputFileName)

    # Display histogram of quantized regions
    histogramImageFileName = outputFileName.replace('.hst', '.png')
    displayHistogram(quantizedBlocks, n, imageFile=histogramImageFileName)
