import cv2
import math
import numpy as np
import re
from os import listdir
from os.path import isfile,join,basename


def log (message):
    print("\n" + message)

def showFiles(files):
	print('======= List of Files =======')
	print('\n'.join(str(p) for p in files))
	print('===================================')
	return

def safeGetDirectory():
	while 1:
		try:
			rootDir = raw_input('Please enter the path where files are located: ')
			validate = raw_input("Directory set to: " + rootDir + " is this okay? Y/N    ")
			if(validate == 'Y' or validate == 'y'):
				return rootDir
		except:
			log("Directory not found!")

def getFile(files):
    showFiles(files)
    while 1:
        try:
            fileName = raw_input("Enter the name of the file you would like to process: \n")
            validate = raw_input("File set to: " + fileName + " is this okay? Y/N:   ")
            if validate == 'y' or validate == 'Y':
                if fileName in files:
                    return fileName
        except:
            log("File not found, please choose another file.")



def getContent(video):
    frameNum = 0
    #totalMax = 0
    #totalMin = 0
    frameData = list()
    while(video.isOpened()):
        ret, frame = video.read()
        if ret:
            frameNum +=1
            frameData.append("Frame: " + str(frameNum))
            yFrameValues = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #frameMax = np.amax(yFrameValues)
            #frameMin = np.amin(yFrameValues)
            #if frameMax > totalMax:
            #    totalMax = frameMax
            #if frameMin < totalMin:
            #   totalMin = frameMin
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
            log(str(option) + " is not a valid input. Please try again.\n")


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

#From the smart people on stackoverflow
#http://stackoverflow.com/questions/16856788/slice-2d-array-into-smaller-2d-arrays
def blockshaped(arr, nrows, ncols):
    """
    Return an array of shape (n, nrows, ncols) where
    n * nrows * ncols = arr.size

    If arr is a 2D array, the returned array should look like n subblocks with
    each subblock preserving the "physical" layout of arr.
    """
    h, w = arr.shape
    return (arr.reshape(h//nrows, nrows, -1, ncols)
               .swapaxes(1,2)
               .reshape(-1, nrows, ncols))

def calculateCoordinates(width, index):
    x = 0
    y = 0
    blockLength = 8
    x = (blockLength*index) % width
    y = math.floor(((blockLength*index)/width) * blockLength)   #calculate y
    return x,y


def quantize(frameData, fileName):
    m = 7 #getMValue()
    print("Running quantization with " + str(m) + " bins...")

    #saving some processing power here so we dont need to calculate these values for each iteration
    result = list()
    bins = pow(2,m)
    frameNum = 0

    #for each entry in frameData
    for i in range(len(frameData)):
        if "Frame" in frameData[i]:
            frameNum = frameData[i].replace("Frame: ", "")
            continue

        frameRegions = blockshaped(frameData[i],8,8)
        #for each region of the frame
        for j in range(len(frameRegions)):
            x,y = calculateCoordinates(len(frameData[i][0]), j)
            result.append(quantizeRegion(frameRegions[j], bins, frameNum, x, y))
            print("processed region " + str(j) + " of frame " + frameNum)
    outputFile = open(fileName, 'w')
    writeToFile(outputFile,result)
    outputFile.close()
    return fileName


def writeToFile(outputFile,content):
    rows = len(content)
    for i in range(rows):
        outputFile.write(content[i])
    return

'''
Main Method
Prompts the user for an input file, a quantization option selection, and an m value.
Uses these values to quantize the input files error into 2^m uniform bins.
'''
if __name__ == '__main__':
    rootDir = '/home/perry/Desktop/CSE408/multimedia-information-systems/test/project1'##safeGetDirectory()
    allFiles = [f for f in listdir(rootDir) if isfile(join(rootDir,f))]
    input_file = '3.mp4'#getFile(allFiles)

    fileName = rootDir + "/" + input_file
    video = cv2.VideoCapture(fileName)

    #frameData, totalMin, totalMax = getContent(video) #this is for quantization at video level
    frameData = getContent(video)

    outputName = quantize(frameData, fileName)
    log(basename(outputName) + " created in location " + rootDir)

    '''
    USE THIS FOR DOCUMENTATION, DO NOT REMOVE YET
    iterate through error array

    for e in errors
      for instance: e = 40

    (40 - (-139)) / 4.1
    (179) / 4.1
    43.24235 <= this number is the number of bins e is greater than min
    43 = floor(e - min / 4.1)
    44

    -139 + 43*4.1 = 37.3
    -139 + 44*4.1 = 41.4
    37.3 + 41.4 / 2 = 39.35


    representative => -139 + 43.5*4.1

    set e = representative

    move on to next e


    | . | . | . | . | .e| . |

    => the number of bins away the current error e is from the bottom
    => gives us i
    '''
