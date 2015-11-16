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
	# frames = np.ndarray(shape = (frameCount,videoHeight,videoWidth,3),dtype = np.uint8)
	frames = []
	# count = 1
	while video.isOpened():
		# print count
		ret,frame = video.read()

		if ret:
			pass
			frames.append(frame)
		else:
			break
		# count += 1

	return frames


rootDir = "C:\Users\Crispino\Documents\GitHub\multimedia-information-systems\\test\project1"
videoName = "2.mp4"

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

# differences = np.zeros(shape = (frameCount - 1,8,8),dtype = np.int16)

for i in range(0,videoHeight,8):
	print i
	for j in range(0,videoWidth,8):
		#temporary_array
		#CHANGE THAT TO OUTSIDE THE LOOPS
		#TRY TO CHANGE THAT TO 8 BYTES
		differences = np.zeros(shape = (frameCount - 1,8,8),dtype = np.int16)
		# differences.fill(0)
		for k in range(0,frameCount - 1):
			yFrameValues = cv2.cvtColor(frames[k],cv2.COLOR_RGB2GRAY)
			yFrameValues = yFrameValues[i:i + 8,j:j + 8]
			yFrameValues = yFrameValues.astype(np.int8)#==================

			if (k == 0):
				differences[k] = np.copy(yFrameValues)
				oldFrame = np.copy(differences[k])
				continue
			elif (k == 1):
				secondFrame = np.copy(yFrameValues)

			differences[k] = np.array(oldFrame - yFrameValues)
			
			oldFrame = np.copy(yFrameValues)


			count += 1

		differences_dic[i,j] = differences

# cv2.destroyAllWindows()

# print count
# print 
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

showReconstructedVideo(differences_dic,videoHeight,videoWidth)
