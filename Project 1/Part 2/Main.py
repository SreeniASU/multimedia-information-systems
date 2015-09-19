import numpy as np
import cv2
from os import listdir
from os.path import isfile,join

def log(message):
	print("--------------------------------------------------------------")
	print(message)
	print("--------------------------------------------------------------")
	return

def displayImage(title,image):
	cv2.imshow(title,image)
	log("Press any key while viewing image to close image and proceed")
	cv2.waitKey(0)
	
def colormap2lut(colormap) :
	# for more information see Part 1 by Jake Pruitt
    times = 256 / len(colormap)
    lut = np.zeros((256, 1, 3), dtype=np.uint8)
    for i in xrange(0, len(colormap)):
        for j in xrange(0, times):
            lut[times*i+j][0] = colormap[i]

    return lut

def scaleImage(image) :
	log("Start - Scaling delta image to from -1 to 1")
	high = 1.0															# our high value
	low = -1.0															# our low value

	mins = np.min(image, axis=0)										# find the min of our image
	maxs = np.max(image, axis=0)										# and the max
	rng = maxs - mins													# calculate the range

	scaled_points = high - (((high - low) * (maxs - image)) / rng)		# and scale our image with these values
	log("Finished - Scaling delta image to from -1 to 1")

	return scaled_points


def getNumberOfFrames(vid):
	log("Start - Gathering frames from the video")
	counter = 1

	while(vid.isOpened()):
		ret,frame = vid.read()

		if ret:
			counter += 1
		else:
			vid.release()
			break
	log("Finished - Gathering frames from the video")

	return counter - 1

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

def getFramesFromSelectedVideo():
	videoName = ""
	while(1):
		try:
			videoName = raw_input('Enter the name of the file you wish to read: ')
			videoName = rootDir + '/' + videoName
			validate = raw_input(videoName + " has been selected for processing is this okay? Y/N    ")
			if(validate == 'Y' or validate == 'y'):
				video = cv2.VideoCapture(videoName)
				if video.isOpened():
					break
				else:
					log("Cannot open specified video")
					videoName = ""
			else:
				videoName = ""
		except:
			log("Unable to open video")

	#function to get the number of frames of a video

	video = cv2.VideoCapture(videoName)
	n_frames = getNumberOfFrames(video)
	video = cv2.VideoCapture(videoName) #we have to get the capture again after the 'getNumberOfFrames' function


	#initialization of 'frame1Read' and 'frame2Read' variables
	frame1Read = n_frames + 1
	frame2Read = n_frames + 1

	#while loop to validate user input
	while (frame1Read > n_frames or frame2Read > n_frames or frame1Read <= 0 or frame2Read <= 0):
		print("Number of frames of the video: " + str(n_frames))
		frame1Read = int(raw_input("Enter the first frame to compare: "))
		frame2Read = int(raw_input("Enter the second frame to compare: "))

		if (frame1Read > n_frames or frame2Read > n_frames):
			raw_input('Invalid frame number(s)!')

	count = 1

	gray1 = ""
	gray2 = ""

	while(video.isOpened()):
		ret,frame = video.read()
		if ret: #if video is still running...
			if frame1Read == count:
				log("Grabbing and converting frame 1 to grayscale")
				gray1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			elif frame2Read == count:
				log("Grabbing and converting frame 2 to grayscale")
				gray2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			count += 1
		else:
			break
	
	return (gray1,gray2)

def getColorImage(image):
	while(1):
		colorMapFileName = raw_input('Please select a colormap for processing: ') 	# prompt user for input
		colorMapFileName = rootDir + '/' + colorMapFileName							# append / for path
		try:
			file = open(colorMapFileName, 'r')										# open the file
			colorMap = eval(file.read())											# read in the values
			lut = colormap2lut(colorMap)											# generate a look up table from the map
			deltaColorFormat = cv2.cvtColor(gray_delta, cv2.COLOR_GRAY2RGB)			# set the colorspace of our image to RGB

			colorImage = cv2.LUT(deltaColorFormat,lut)								# apply the colormap from the LUT

			return colorImage

		except:
			log("Unable to open file")



#  ============================================================================================
#  										MAIN FUNCTION BODY
#  ============================================================================================
#get the directory from the user
rootDir = safeGetDirectory()

#find all the files in this directory
onlyfiles = [ f for f in listdir(rootDir) if isfile(join(rootDir,f))]
showFiles(onlyfiles)

#Prompt user for a video and two frames, then get those two frames and convert to grayscale
gray1,gray2 = getFramesFromSelectedVideo()

	
displayImage('Frame 1 Grayscale',gray1)

displayImage('Frame 2 Grayscale',gray2)

cv2.destroyAllWindows()

#calculate our difference image delta
gray_delta = gray1 - gray2
displayImage('Delta Image',gray_delta)

#calculate the scaled image
scaled_points = scaleImage(gray_delta)
displayImage('Scaled Delta Image',scaled_points)

showFiles(onlyfiles)

#Create a color image out of the passes image
colorImage = getColorImage(scaled_points)

displayImage('final_image',colorImage)

cv2.destroyAllWindows()
