import cv2
import math
import numpy as np
import matplotlib.pyplot as plt
import re
import Utility as util
from os import listdir
from os.path import isfile,join,basename

def getContent(video):
    frameNum = 0
    frameData = list()
    while(video.isOpened()):
        ret, frame = video.read()
        if ret:
            frameNum +=1
            frameData.append("Frame: " + str(frameNum))
            yFrameValues = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frameData.append(yFrameValues)
        else:
            break
    return frameData#, totalMin, totalMax



def getMValue():
      while 1:
        try:
            option = input("Please enter an m value: ")
            if option < 1:
                print(str(option) + " is not a valid selection. Please make a different selection.\n")
            else:
                return option
        except:
            print(str(option) + " is not a valid input. Please try again.\n")

'''
Quantizes a region using the number of bins
Returns a formatted string for output to a file which details the information in the format:
< FrameNumber, (X coordinate, Y coordinate) , Y Channel Value, Number Of Occurances >
'''
def quantizeRegion(region, bins, frameNum, x, y):
    minValue = np.amin(region)
    maxValue = np.amax(region)
    valueRange = maxValue - minValue    #quantization is block level so find these values here
    valuesPerBin = valueRange / bins    #problem here when bin is greater than range
    if(valueRange < bins):
        valuesPerBin = 1
    occurancesInFrame = dict.fromkeys(range(minValue, maxValue + 1), 0) #dictionary to contain how many times a value occurs
    rows = len(region)
    cols = len(region[0])
    resultString = ""

    for i in range(rows):
        for j in range(cols):
            bottomBin = math.floor((region[i][j] - minValue) / valuesPerBin)
            occurancesInFrame[math.floor(minValue + (bottomBin + 0.5)*valuesPerBin)] += 1

    for key in occurancesInFrame:
        if occurancesInFrame[key] > 0:   #for testing dont write 0 values
            resultString += "< " + str(frameNum) + ", (" + str(x) + ", " + str(y) + ") ," + str(key) + ", " + str(occurancesInFrame[key]) + " >\n"
    return resultString

'''
From the smart people on stackoverflow
http://stackoverflow.com/questions/16856788/slice-2d-array-into-smaller-2d-arrays

Return an array of shape (n, nrows, ncols) where
    n * nrows * ncols = arr.size

    If arr is a 2D array, the returned array should look like n subblocks with
    each subblock preserving the "physical" layout of arr.
'''
def blockshaped(arr, nrows, ncols):
    return (arr.reshape(h//nrows, nrows, -1, ncols)
               .swapaxes(1,2)
               .reshape(-1, nrows, ncols))

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


def quantize(frameData, fileName):
    m = 128 #getMValue()
    print("Running quantization with " + str(m) + " bins...")

    #saving some processing power here so we dont need to calculate these values for each iteration
    result = list()
    frameNum = 0

    #for each entry in frameData
    for i in range(len(frameData)):
        if "Frame" in frameData[i]:
            frameNum = frameData[i].replace("Frame: ", "")
            print("Processing regions of frame: " + frameNum)
            continue

        frameRegions = blockshaped(frameData[i],8,8)
        if i == 1:
            print (str(len(frameRegions)) + " regions per frame.")
        #for each region of the frame
        for j in range(len(frameRegions)):
            x,y = calculateCoordinates(len(frameData[i][0]), j)
            result.append(quantizeRegion(frameRegions[j], m, frameNum, x, y))

    print("Creating histogram.")
    createHistogram(result, False, m)
    fileName = fileName.replace(".mp4","_hist_" + str(m) + ".hst")
    outputFile = open(fileName, 'w')
    util.writeToFile(outputFile,result)
    outputFile.close()
    return fileName


def createHistogram(input, fromFile, m):
    '''
    < 1, (0, 0.0) ,136, 1 >
    < 1, (0, 0.0) ,139, 1 >
    < 1, (0, 0.0) ,146, 1 >
    < 1, (0, 0.0) ,153, 1 >
    < 1, (0, 0.0) ,155, 1 >
    < 1, (0, 0.0) ,156, 3 >
    '''
    content = list();
    histDict = dict.fromkeys(range(0, 256), 0)
    if fromFile:
     with open(input,'r') as f:
        content = f.readlines()

    for i in range(len(input)):
        content = input[i].split('\n')
        for j in range(len(content) -2 ):
            remove = re.search("<\s*\d*\,\s*\(\d*\,\s*\d*\)\s*\,\s*",content[j])
            key,val = content[j].replace(remove.group(0),"").replace(">","").split(',')
            histDict[int(key)] += int(val) # += int(val)  #increment the value at the key by the given

    plt.hist2d(histDict.keys(), histDict.values(), m) #need to add bars maybe? not sure here
    print("Press any key or click to continue.")
    plt.waitforbuttonpress()
    #need to suppress these dumb errors from pointer event

'''
Main Method
Prompts the user for an input file, a quantization option selection, and an m value.
Uses these values to quantize the input files error into 2^m uniform bins.
'''
if __name__ == '__main__':
    rootDir = '/home/perry/Desktop/multimedia/multimedia-information-systems/test/project1'##util.safeGetDirectory()
    allFiles = [f for f in listdir(rootDir) if isfile(join(rootDir,f))]
    input_file = 'R2.mp4'#util.getFile(allFiles)

    fileName = rootDir + "/" + input_file
    video = cv2.VideoCapture(fileName)

    #frameData, totalMin, totalMax = getContent(video) #this is for quantization at video level
    frameData = getContent(video)
    outputName = quantize(frameData, fileName)
    print(basename(outputName) + " created in location " + rootDir)
