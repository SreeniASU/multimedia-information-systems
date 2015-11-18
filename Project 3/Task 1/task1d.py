import numpy as np
import cv2
import os

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
	# frames = np.zeros(shape = (frameCount,videoHeight,videoWidth,3),dtype = np.uint8)
	frames = []
	# count = 1
	while video.isOpened():
		# print count
		ret,frame = video.read()

		if ret:
			frames.append(frame)
		else:
			break
		# count += 1

	return frames

def outputFrameInformation(differences,blockCoordX,blockCoordY):
	#iterates throught the 8x8 'differences' array containing differences frames and outputs
	#those differences to an output string
	#blockCoordX,blockCoordY are the x,y coordinate for the block where the frames in
	#the 'differences' array are located
	outputString = ""
	dic = {}

	for i in range(0,len(differences)):
		frame = differences[i]
		frame_id = i
		for j in range(0,len(frame)):
			for k in range(0,len(frame[j])):
				diffValue = frame[j][k]
				pixelCount = updateDictionaryValueCount(dic,blockCoordX,blockCoordY,diffValue)
				outputString += "<" + str(frame_id) + ",(" + str(blockCoordX) + "," + str(blockCoordY) + ")," + str(diffValue) +"," + str(pixelCount) + ">\n"

	return outputString

def updateDictionaryValueCount(dic,blockCoordX,blockCoordY,val):
	#updates the count of value 'val' located on the block of corrdinates "blockCoordX,blockCoordY"
	#on dictionary 'dic'

	try:
		dic[blockCoordX,blockCoordY,val] += 1
	except KeyError:
		dic[blockCoordX,blockCoordY,val] = 1

	return dic[blockCoordX,blockCoordY,val]


def writeToFile(videoName,outputString,n,type):
	if type == 0:
		mode = 'w'
	if type == 1:
		mode = 'a'

	fileName = videoName + '_diff_' + str(n) + '.dhc'
	outputFile = open(fileName,mode)
	outputFile.write(outputString);

	outputFile.close()

rootDir = "C:\Users\Crispino\Documents\GitHub\multimedia-information-systems\\test\project1"
videoName = "6.mp4"

videoPath = os.path.join(rootDir,videoName)

video = cv2.VideoCapture(videoPath)

videoHeight = int(video.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
videoWidth = int(video.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
frameCount = int(video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))

print videoWidth,videoHeight,frameCount
print

count = 1
# global differences
differences_dic = {}
#--------------------------------
global secondFrame
#--------------------------------
oldFrame = np.zeros(shape = (8,8),dtype = np.int8)

frames = getListOfFrames(video,frameCount,videoHeight,videoWidth)
video.release()
print len(frames)

outputString = ""
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
		for k in range(0,frameCount - 1):
			yFrameValues = cv2.cvtColor(frames[k],cv2.COLOR_RGB2GRAY)
			yFrameValues = yFrameValues[i:i + 8,j:j + 8]
			# yFrameValues = yFrameValues.astype(np.int8)#==================
			yFrameValues = yFrameValues.astype(np.int16)

			if (k == 0):
				differences[k] = np.copy(yFrameValues)
				oldFrame = np.copy(differences[k])
				continue
			elif (k == 1):
				secondFrame = np.copy(yFrameValues)

			differences[k] = np.array(oldFrame - yFrameValues)
			
			oldFrame = np.copy(yFrameValues)

			del yFrameValues

			count += 1

		outputString += outputFrameInformation(differences,i,j)
		#REMOVE THAT WHEN NOT RECONSTRUCTING THE VIDEO
		#------------------------------------------------
		differences_dic[i,j] = differences
		#------------------------------------------------
		if (i == 0 and j == 0):
			writeToFile(videoName,outputString,0,0)
		else:
			writeToFile(videoName,outputString,0,1)
		del outputString


#logging for testing purposes
print differences
print len(differences)
print
print "first frame: "
print differences[0]
print 
print "second frame: "
print secondFrame
print "difference between first and second frame: "
print differences[1]
print 'count: ' + str(count)
print "press enter"

print frameCount,videoHeight,videoWidth
print len(differences_dic)

#used just for testing: 
# showReconstructedVideo(differences_dic,videoHeight,videoWidth)