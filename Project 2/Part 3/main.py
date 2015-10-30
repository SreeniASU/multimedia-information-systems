import cv2
import math
import numpy as np
from os import listdir
from os.path import isfile,join

def getOption():
    while 1:
        try:
            option = input("Which quantization option would you like to use?\n" +
                         "1: No quantization\n" +
                         "2: Quantization into 2^m uniform bins\n>")
            if option > 2 or option < 1:
                print(str(option) + " is not a valid selection. Please make a different selection.\n")
            else:
                log("Option: " + str(math.floor(option)) + " selected.")
                return math.floor(option)
        except:
            log(str(option) + " is not a valid input. Please try again.\n")

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


def getErrors(content):
    rows = len(content)
    errors = []
    for i in range(rows):
        if content[i][0] != "{":
            errors.append(float(content[i].split(",")[3].replace(">", "")))
    return errors


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

def quantizeWithM(errors,m):
    minError = min(errors)
    maxError = max(errors)
    bins = pow(2,m)
    rangeError = maxError - minError
    valuesPerBin = rangeError / bins

    rows = len(errors)
    for i in range(rows):
        bottomBin = math.floor((errors[i] - minError) / valuesPerBin)
        errors[i] = minError + (bottomBin + 0.5)*valuesPerBin

    return errors

def writeToFile(outputFile,content, errors):
    rows = len(content)
    j = 0
    for i in range(rows):
        if content[i][0] != "{":
            error = content[i].split(",")[3]
            beginning = content[i].split(error)[0]
            content[i] = beginning + str(errors[j]) + " >"
            j += 1

        outputFile.write(content[i] + "\n")

    return


'''
Main Method
Prompts the user for an input file, a quantization option selection, and an m value.
Uses these values to quantize the input files error into 2^m uniform bins.
'''
rootDir = safeGetDirectory()

allFiles = [f for f in listdir(rootDir) if isfile(join(rootDir,f))]

input_file = getFile(allFiles)

fileName = rootDir + "/" + input_file

with open(fileName,'r') as f:
	content = f.readlines()

errors = getErrors(content)

option = getOption()

if option == 2:
    m = getMValue()
    errors = quantizeWithM(errors,m)
    if "tpc" in fileName:
        fileName = fileName.strip(".tpc") + "_" + str(m) + ".tpq"
    elif "spc" in fileName:
        fileName = fileName.strip(".spc") + "_" + str(m) + ".spq"

elif option == 1:
    if "tpc" in fileName:
        fileName = fileName.strip(".tpc") + "_" + str(m) + ".tpq"
    elif "spc" in fileName:
        fileName = fileName.strip(".spc") + "_" + str(m) + ".spq"

outputFile = open(fileName, 'w')
writeToFile(outputFile,content,errors)
log(fileName.strip(rootDir) + " created in location " + rootDir)
outputFile.close()


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



    












