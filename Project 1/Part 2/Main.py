import numpy as np
import cv2
import pickle

#function to get the number of frames of a video
def getNumberOfFrames(vid):
	counter = 1

	while(vid.isOpened()):
		ret,frame = vid.read()

		if ret:
			counter += 1
		else:
			vid.release()
			break

	return counter - 1

video = cv2.VideoCapture('1.mp4')

n_frames = getNumberOfFrames(video)

video = cv2.VideoCapture('1.mp4') #we have to get the capture again after the 'getNumberOfFrames' function

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
			#cv2.imshow('frame1Read',frame)
			#cv2.waitKey(0)
			gray1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			#cv2.waitKey(0)
			#cv2.imwrite('frame' + str(frame1Read) + '.png',frame)
		elif frame2Read == count:
			gray2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			#cv2.imshow('frame2Read',frame)
			#cv2.waitKey(0)
			#cv2.imwrite('frame' + str(frame2Read) + '.png',frame)

		count += 1
	else:
		break

cv2.imshow('frame1',gray1)
cv2.waitKey(0)

cv2.imshow('frame2',gray2)
cv2.waitKey(0)
cv2.destroyAllWindows()

gray_delta = gray1 - gray2

cv2.imshow('delta',gray_delta)
cv2.waitKey(0)

#new_image = cv2.cvtColor(gray_delta,cv2.CV_32F)
#cv2.imshow('delta',new_image)
#cv2.waitKey(0)

#gray1.convertTo(dst, CV_32F)

high = 1.0
low = -1.0

mins = np.min(gray_delta, axis=0)
maxs = np.max(gray_delta, axis=0)
rng = maxs - mins

scaled_points = high - (((high - low) * (maxs - gray_delta)) / rng)

#text_file = open('new_grayscale.txt','w')

#text_file.write(gray_delta)

#text_file.write('\n\n\n %s' % scaled_points)

f = open("new_grayscale.txt", "w")
f.write("".join(map(lambda x: str(x), scaled_points)))
f.close()

#print("gray delta new: ",scaled_points)
cv2.imshow('gray delta new',scaled_points)
cv2.waitKey(0)

print(count)

video.release()
cv2.destroyAllWindows()