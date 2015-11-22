import cv2
import math
import numpy as np
import matplotlib.pyplot as plt
import re
import Utility as util
from os import listdir
from os.path import isfile,join,basename

def getContent(video):
    frameData = list()
    while(video.isOpened()):
        ret, frame = video.read()
        if ret:
            yFrameValues = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frameData.append(yFrameValues)
        else:
            break
    # Possibly revisit to add max and min here
    return frameData



def getMValue():
      while 1:
        try:
            option = input('Please enter an m value: ')
            if option < 1:
                print(str(option) + ' is not a valid selection. Please make a different selection.\n')
            else:
                return option
        except:
            print(str(option) + ' is not a valid input. Please try again.\n')

'''
Quantizes a block using the number of bins
Returns a formatted string for output to a file which details the information in the format:
< FrameNumber, (X coordinate, Y coordinate) , Y Channel Value, Number Of Occurances >
'''
def quantizeBlock(block, bins, frameNum, x, y):
    minValue = np.amin(block)
    maxValue = np.amax(block)
    samples, valuesPerBin = np.linspace(minValue, maxValue, bins, endpoint=False, retstep=True)
    occurancesInFrame = dict.fromkeys(samples, 0) #dictionary to contain how many times a value occurs
    result = list()

    for val in np.nditer(block):
        if valuesPerBin == 0:
            bottomBin = minValue
        else:
            bottomBin = minValue + math.floor((val - minValue) / valuesPerBin) * valuesPerBin

        if bottomBin == maxValue:
            bottomBin -= valuesPerBin
        occurancesInFrame[bottomBin] += 1

    for key in occurancesInFrame:
        result.append({
            'frameNum': frameNum,
            'blockCoords': (x, y),
            'key': key,
            'val': occurancesInFrame[key]
        })

    return result

'''
Find the coordinates of the given region by utilizing the index and width of the video
'''
def calculateCoordinates(width, index):
    x = 0
    y = 0
    blockLength = 8
    x = (blockLength*index) % width
    y = int(math.floor(((blockLength*index)/width) * blockLength))
    return x,y


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
    util.writeToFile(outputFile,quantizedFrameBlocks)
    outputFile.close()

def displayHistogram(input, n, fromFile=False):
    '''
    < 1, (0, 0.0) ,136, 1 >
    < 1, (0, 0.0) ,139, 1 >
    < 1, (0, 0.0) ,146, 1 >
    < 1, (0, 0.0) ,153, 1 >
    < 1, (0, 0.0) ,155, 1 >
    < 1, (0, 0.0) ,156, 3 >
    '''
    print('Creating histogram.')
    content = list();
    histDict = dict.fromkeys(range(0, 256), 0)
    if fromFile:
        with open(input,'r') as f:
            content = f.readlines()

    for i in range(len(input)):
        content = input[i].split('\n')
        for j in range(len(content) -2 ):
            remove = re.search('<\s*\d*\,\s*\(\d*\,\s*\d*\)\s*\,\s*',content[j])
            key,val = content[j].replace(remove.group(0),'').replace('>','').split(',')
            histDict[int(key)] += int(val) # += int(val)  #increment the value at the key by the given

    plt.hist2d(histDict.keys(), histDict.values(), m) #need to add bars maybe? not sure here
    print('Press any key or click to continue.')
    plt.waitforbuttonpress()
    #need to suppress these dumb errors from pointer event

'''
Main Method
Prompts the user for an input file, a quantization option selection, and an m value.
Uses these values to quantize the input files error into 2^m uniform bins.
'''
if __name__ == '__main__':
    rootDir = util.safeGetDirectory()
    allFiles = [f for f in listdir(rootDir) if isfile(join(rootDir,f))]
    input_file = util.getVideoFile(allFiles)

    # User input instead
    n = 32

    # Read video data
    fileName = rootDir + '/' + input_file
    video = cv2.VideoCapture(fileName)
    frameData = getContent(video)

    # Quantize the blocks of the video
    quantizedBlocks = quantize(frameData, n)

    # Write the data to the file
    outputFileName = fileName.replace('.mp4','_hist_' + str(n) + '.hst') 
    writeHistogramToFile(quantizedBlocks, outputFileName)

    # Display histogram of quantized regions
    displayHistogram(quantizedBlocks, n)
