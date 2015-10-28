import cv2
import math
import numpy as np
from os import listdir
from os.path import isfile,join

def minValue():
	pass

def maxValue():
	pass

def log (message):
    print(message)

def showFiles(files):
	print('======= List of Files =======')
	print('\n'.join(str(p) for p in files))
	print('===================================')
	return

def safeGetDirectory():
	while 1:
		try:
			rootDir = raw_input('Please enter the path where video files are located: ')
			validate = raw_input("Directory set to: " + rootDir + " is this okay? Y/N    ")
			if(validate == 'Y' or validate == 'y'):
				return rootDir
		except:
			log("Directory not found!")

def getVideoFile(files):
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


# m = 8


# rootDir = safeGetDirectory()
rootDir = '/Users/jake/Projects/multimedia-information-systems/Project 2/Part 1'

allFiles = [f for f in listdir(rootDir) if isfile(join(rootDir,f))]

# input_file = getVideoFile(allFiles)
input_file = "3_3.tpc"

fileName = rootDir + "/" + input_file

with open(fileName,'r') as f:
	content = f.readlines()

rows = len(content)
errors = []
for i in range(rows):
    if content[i][0] != "{":
        errors.append(float(content[i].split(",")[3].replace(">", "")))

minError = min(errors)
maxError = max(errors)
print(minError)
print(maxError)

m = input("Please enter m: ")
bins = pow(2,m)

rangeError = maxError - minError
valuesPerBin = rangeError / bins

rows = len(errors)
for i in range(rows):
    bottomBin = math.floor((errors[i] - minError) / valuesPerBin)
    errors[i] = minError + (bottomBin + 0.5)*valuesPerBin


rows = len(content)
j = 0
fileName = fileName.strip(".tpc") + "_" + str(m) + ".spq"
outputFile = open(fileName, 'w')
for i in range(rows):
    if content[i][0] != "{":
        error = content[i].split(",")[3]
        beginning = content[i].split(error)[0]
        content[i] = beginning + str(errors[j]) + " >"
        j += 1

    outputFile.write(content[i] + "\n")

outputFile.close()


'''

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



    












