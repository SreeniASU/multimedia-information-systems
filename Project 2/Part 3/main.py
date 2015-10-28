import cv2
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


rootDir = safeGetDirectory()
# rootDir = 'C:\Users\Crispino\Documents\GitHub\multimedia-information-systems\Project 2\Part 1'

allFiles = [f for f in listdir(rootDir) if isfile(join(rootDir,f))]

input_file = getVideoFile(allFiles)

fileName = rootDir + "/" + input_file

with open(fileName,'r') as f:
	content = f.readlines()

