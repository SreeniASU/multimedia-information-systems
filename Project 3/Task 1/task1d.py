import numpy as np
import cv2
import os
import re
import matplotlib.pyplot as plt
import Utility as util

#gets the Y values of a frame
def getYValues(frame):
	#creates the array that will contain the Y values
	yFrameValues = np.ndarray(shape = (len(frame),len(frame[0])),dtype = np.int16)#type(frame)

	#converts original frame to the YUV color space
	yFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2YUV)

	#iterates through the YUV frame to get only the Y values
	for row in range(0,len(yFrame)):
		for column in range(0,len(yFrame[row])):
			yFrameValues[row][column] = yFrame[row][column][0]

	return yFrameValues

def showReconstructedVideo(differences_dic,videoHeight,videoWidth):
	global tmpDifferences,differences

	for i in range(0,videoHeight,8):
		for j in range(0,videoWidth,8):
			print i,j
			if (j == 0):
				tmpDifferences = np.copy(differences_dic[i,j])
			else:
				tmpDifferences = np.concatenate((tmpDifferences,differences_dic[i,j]),axis = 2)

		if (i == 0):
			differences = np.copy(tmpDifferences)
		else:
			differences = np.concatenate((differences,tmpDifferences),axis = 1)

		print differences.shape
	print "\nShape of differences array: "
	print differences.shape #must be (nFrames,heigth,width)
	print 

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

def getListOfFrames(video,frameCount,videoHeight,videoWidth):
	frames = []
	while video.isOpened():
		ret,frame = video.read()

		if ret:
			frames.append(frame)
		else:
			break

	return frames

def outputFrameInformation(differences,blockCoordX,blockCoordY,dicValuesTotal):
	#iterates throught the 8x8 'differences' array containing differences frames and outputs
	#those differences to an output string
	#blockCoordX,blockCoordY are the x,y coordinate for the block where the frames in
	#the 'differences' array are located
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


def createHistogram(input, fromFile, histDict, m):
#NEED TO CHANGE THAT
#MAYBE COMMENTED CODE IS NOT USEFUL
    '''
    < 1, (0, 0.0) ,136, 1 >
    < 1, (0, 0.0) ,139, 1 >
    < 1, (0, 0.0) ,146, 1 >
    < 1, (0, 0.0) ,153, 1 >
    < 1, (0, 0.0) ,155, 1 >
    < 1, (0, 0.0) ,156, 3 >
    '''

    content = list();
    # histDict = dict.fromkeys(range(-256, 256), 0)

    if fromFile:
     with open(input,'r') as f:
        content = f.readlines()

    # for i in range(len(input)):
    #     content = input[i].split('\n')
    #     for j in range(len(content) -2 ):
    #         remove = re.search("<\s*\d*\,\s*\(\d*\,\s*\d*\)\s*\,\s*",content[j])
    #         key,val = content[j].replace(remove.group(0),"").replace(">","").split(',')
    #         histDict[int(key)] += int(val) # += int(val) increment the value at the key by the given

    plt.hist2d(histDict.keys(), histDict.values(), m) #need to add bars maybe? not sure here
    print("Press any key or click to continue.")
    plt.waitforbuttonpress()
    #need to suppress these dumb errors from pointer event


def writeToFile(videoName,outputString,n,type):
	#writes the string "outputString" information to a file
	#'n' argument is the n supplied by the user
	#'type' defines if the function uses write mode or append mode
	#if 'type' is 0, write mode is used. If 'type' is 1, append mode is used.

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

print videoWidth,videoHeight,frameCount
print

differences_dic = {}

#dictionary that contains count of how many times each difference frame value appear on the video
valuesDic = dict.fromkeys(range(-256, 256), 0)

n = 128
oldFrame = np.zeros(shape = (8,8),dtype = np.int8)

# frames = getListOfFrames(video,frameCount,videoHeight,videoWidth)

outputString = ""
outputContainer = list()
# differences = np.zeros(shape = (frameCount - 1,8,8),dtype = np.int16)

for i in range(0,videoHeight,8):
	print i
	for j in range(0,videoWidth,8):
		#temporary_array
		#CHANGE THAT TO OUTSIDE THE LOOPS
		#TRY TO CHANGE THAT TO 8 BYTES
		differences = np.zeros(shape = (frameCount - 1,8,8),dtype = np.int16)
		# differences.fill(0)
		outputString = ""

		video = cv2.VideoCapture(videoPath)

		for k in range(0,frameCount - 1):
			# yFrameValues = cv2.cvtColor(frames[k],cv2.COLOR_RGB2GRAY)
			_,frame = video.read()

			yFrameValues = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
			yFrameValues = yFrameValues[i:i + 8,j:j + 8]
			yFrameValues = yFrameValues.astype(np.int16)

			if (k == 0):
				differences[k] = np.copy(yFrameValues)
				oldFrame = np.copy(differences[k])
				continue

			differences[k] = np.array(oldFrame - yFrameValues)
			
			oldFrame = np.copy(yFrameValues)

			del yFrameValues


		video.release()

		outputString += outputFrameInformation(differences,i,j,valuesDic)

		outputContainer.append(outputString)
		#REMOVE THAT WHEN NOT RECONSTRUCTING THE VIDEO
		#------------------------------------------------
		differences_dic[i,j] = differences
		#------------------------------------------------
		if (i == 0 and j == 0):
			writeToFile(videoName,outputString,0,0)
		else:
			writeToFile(videoName,outputString,0,1)

		#clear data from outputString
		del outputString

print "Data outputed to file!"

raw_input("Press enter to show the histogram: ")
createHistogram(outputContainer,False,valuesDic,n)

#used just for testing: 
# showReconstructedVideo(differences_dic,videoHeight,videoWidth)