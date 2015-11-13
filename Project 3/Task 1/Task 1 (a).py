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
    totalMax = 0
    totalMin = 0
    frameData = list()
    while(video.isOpened()):
        ret, frame = video.read()
        if ret:
            frameNum +=1
            yFrameValues = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frameMax = np.amax(yFrameValues)
            frameMin = np.amin(yFrameValues)
            if frameMax > totalMax:
                totalMax = frameMax
            if  frameMin < totalMin:
                totalMin = frameMin
            frameData.append(yFrameValues)
        else:
            break
    return frameData, totalMin, totalMax



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




def writeToFile(outputFile,content, errors):
    rows = len(content)
    j = 0
    for i in range(rows):
        result = re.match("(?P<beginning><\d+,\d,\d,)(?P<e>-?\d+(.*)?)\n", content[i])
        if result:
            beginning = result.group('beginning')
            content[i] = beginning + str(errors[j]) + "\n"
            j += 1

        outputFile.write(content[i])

    return

def quantize(frameData, fileName, minValue, maxValue):
    m = getMValue()
    print("Running quantization with " + str(m) + " bins...")
    result = list()
    bins = pow(2,m)
    valueRange = maxValue - minValue
    valuesPerBin = valueRange / bins
    row = 0
    col = 0

    #Beginning idea, need to figure out how I am going to get the region and the framenumber
    occurancesInFrame = dict.fromkeys(range(minValue, maxValue), 0) #dictionary to contain how many times a value occurs
    rows = len(region)
    for i in range(rows):
        occurancesInFrame[region[i]] += 1
        bottomBin = math.floor((region[i] - minValue) / valuesPerBin)
        region[i] = minValue + (bottomBin + 0.5)*valuesPerBin

    for key in occurancesInFrame:
        resultString = "< " + frameNum + ", (" + regionStart + ", " + regionEnd + ") ," + str(key) + ", " + str(occurancesInFrame[key]) + " >"
        result.append()

    outputFile = open(fileName, 'w')
    ##writeToFile(outputFile,content,errors)
    outputFile.close()
    return fileName

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

    frameData, totalMin, totalMax = getContent(video)

    outputName = quantize(frameData, fileName,totalMin,totalMax)
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
