import numpy as np
import cv2
import os
import re
import matplotlib.pyplot as plt
import Utility as util

def showReconstructedVideo(differences_dic,videoHeight,videoWidth):
	'''
	gets the video height, width, and an dictionary that contains an array of frames for each 
	8x8 block of coordinates (x,y), reconstruct that to the original video and displays it.
	Used for test purposes only
	'''
	global tmpDifferences,differences

	for i in range(0,videoHeight,8):
		for j in range(0,videoWidth,8):
			if (j == 0):
				tmpDifferences = np.copy(differences_dic[i,j])
			else:
				tmpDifferences = np.concatenate((tmpDifferences,differences_dic[i,j]),axis = 2)

		if (i == 0):
			differences = np.copy(tmpDifferences)
		else:
			differences = np.concatenate((differences,tmpDifferences),axis = 1)

		print differences.shape
	#logging
	#-----------------------------------------
	print "\nShape of differences array: "
	print differences.shape
	print 
	#-----------------------------------------

	raw_input("press enter to show the video: ")

	start = True
	for diff_frame in differences:
		if start:
			frame = diff_frame.astype(np.uint8)
			start = False
			continue
		else:
			frame = (frame - diff_frame).astype(np.uint8)

		cv2.imshow('nonsense',frame)
		cv2.waitKey(0)

	cv2.destroyAllWindows()

def outputFrameInformation(differences,blockCoordX,blockCoordY,dicValuesTotal):
	'''
	iterates throught the 8x8 'differences' array containing differences frames and outputs
	those differences to an output string
	blockCoordX,blockCoordY are the x,y coordinate for the block where the frames in
	the 'differences' array are located
	'''
	outputString = ""
	#needs to update dictionary so it identificates the frame and the block region of the diff_value

	dicValuesBlock = {}

	for i in range(0,len(differences)):
		frame = differences[i]
		frame_id = i + 1
		for j in range(0,len(frame)):
			for k in range(0,len(frame[j])):
				diffValue = frame[j][k]
				# pixelCount = updateDictionaryValueCount(dic,blockCoordX,blockCoordY,diffValue)
				# outputString += "<" + str(frame_id) + ",(" + str(blockCoordX) + "," + str(blockCoordY) + ")," + str(diffValue) +"," + str(pixelCount) + ">\n"
				updateDictionaryValueCount(dicValuesBlock,frame_id,diffValue)
				dicValuesTotal[diffValue] += 1

	#sorts the dictionary keys for better printing
	sortedDicValuesBlock = sorted(dicValuesBlock.items())


	for i in sortedDicValuesBlock:
		key = i[0]

		frame_id = key[0]
		diff_value = key[1]
		pixelCount = dicValuesBlock[key]

		outputString += "<" + str(frame_id) + ",(" + str(blockCoordX) + "," + str(blockCoordY) + ")," + str(diff_value) +"," + str(pixelCount) + ">\n"


	return outputString

def updateDictionaryValueCount(dic,frame_id,val):
	'''updates the count of value 'val' located on the frame represented by "frame_id"
	on dictionary 'dic' '''

	try:
		dic[frame_id,val] += 1
	except KeyError:
		dic[frame_id,val] = 1


def createHistogram(fromFile, histDict, m):
	'''
		histDict: contains the count of how many times each difference value appears 
		on the whole video.
		
		The function gets data from dictionary "histDict", and creates a histogram
		based on its data.
	'''

	plt.hist2d(histDict.keys(), histDict.values(), m) #need to add bars maybe? not sure here
	print("Press any key or click to continue.")
	plt.waitforbuttonpress()
	#need to suppress these dumb errors from pointer event


def writeToFile(videoName,outputString,n,type):
	'''
	writes the string "outputString" information to a file
	'n' argument is the n supplied by the user
	'type' defines if the function uses write mode or append mode
	if 'type' is 0, write mode is used. If 'type' is 1, append mode is used.

	'''

	if type == 0:
		mode = 'w'
	if type == 1:
		mode = 'a'

	fileName = videoName + '_diff_' + str(n) + '.dhc'
	outputFile = open(fileName,mode)
	outputFile.write(outputString);

	outputFile.close()

rootDir = "C:\Users\Crispino\Documents\GitHub\multimedia-information-systems\\test\project1"
# rootDir = ""
videoName = "R1.mp4"

videoPath = os.path.join(rootDir,videoName)

video = cv2.VideoCapture(videoPath)

videoHeight = int(video.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
videoWidth = int(video.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
frameCount = int(video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))

video.release()

print "Video width: " + str(videoWidth)
print "Video heigth: " + str(videoHeight)
print "Number of frames: " + str(frameCount)

differences_dic = {}

#dictionary that contains count of how many times each difference frame value appear on the video
valuesDic = dict.fromkeys(range(-256, 256), 0)

n = 128
oldFrame = np.zeros(shape = (8,8),dtype = np.int8)

outputString = "" #string used to update output file

#iterates through each 8x8 region and gets 
for i in range(0,videoHeight,8):
	print i
	for j in range(0,videoWidth,8):
		#temporary array that contains the difference frames for the block of the time
		differences = np.zeros(shape = (frameCount - 1,8,8),dtype = np.int16)
		outputString = ""

		#video capture object
		video = cv2.VideoCapture(videoPath)

		#iterating through each frame
		for k in range(0,frameCount - 1):
			#original frame is read here
			_,frame = video.read()

			#frame is converted to grayscale(to get Y values) and cropped to a 8x8 block
			yFrameValues = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
			yFrameValues = yFrameValues[i:i + 8,j:j + 8]
			#array type is changed to support values on the range (-255,255)
			yFrameValues = yFrameValues.astype(np.int16)

			if (k == 0):
				#if it is the first iteration, no differences are calculated
				differences[k] = np.copy(yFrameValues)
				oldFrame = np.copy(differences[k])
				continue
			
			'''
			otherwise, the current difference is calculated by taking the 
			difference of the previous frame and the current one
			'''
			
			differences[k] = np.array(oldFrame - yFrameValues)
			
			oldFrame = np.copy(yFrameValues)

			del yFrameValues


		video.release()

		outputString += outputFrameInformation(differences,i,j,valuesDic)

		#writes current 'outputString' data to file
		if (i == 0 and j == 0):
			writeToFile(videoName,outputString,0,0)
		else:
			writeToFile(videoName,outputString,0,1)

		#then clears data from outputString
		del outputString

print "Data outputed to file!"

raw_input("Press enter to show the histogram: ")
#testing function below without receiving a valid input list
createHistogram(False,valuesDic,n)