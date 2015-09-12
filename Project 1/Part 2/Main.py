#James Perry - 1204873588
#CSE408 Project 1 - Part 2
#=====================================================================================================================
#Description:
#Implement a second program which lets the user select
#- a video file, v, in the database,
#- a frame rate, r,
#- two frames, f1 and f2, and
#- a color map file
#given these,
#- extract and displays 8-bit gray scale contents, g1 and g2, of frames, f1 and f2,
#- compute a difference image, DELTA, of gray scale images, g1 and g2,
#- rescales the values in the difference image to a range between -1.0 and 1.0 (such that -1.0 corresponds to
# 255 and 1.0 corresponds to 255), and
#- visualizes the difference image ? using the selected color map.
#=====================================================================================================================
import numpy as np
import cv2
import os

#directory where files are stored
rootDir = "Tests"
fileSet = set()
fileNameSet = set()

#this extracts all files from our directory
for dir_, _, files in os.walk(rootDir):
    for fileName in files:
        relDir = os.path.relpath(dir_, rootDir)     #get path to directory
        relFile = os.path.join(relDir, fileName)    #get file in that directory
        fileSet.add(relFile)
        relFile = os.path.basename(relFile)         #remove path from name
        fileNameSet.add(relFile)                        #add it to out list of files

#collect our user input for processing
print('======= List of Video Files =======')
print '\n'.join(str(p) for p in fileNameSet)
print('===================================')
#print information to collect user inpput
videoName = raw_input('Enter the name of the file you wish to read: ')
#frameRateRead = raw_input("Enter desired frame rate: ")
frame1Read = raw_input("Enter the first frame to compare: ")
frame2Read = raw_input("Enter the second frame to compare: ")
#colorMapFile = raw_input("Please select a color map file: ")

#need colormap file and framerate support

#get the video by name from our file list
selectedVideo = ""
for file in fileSet:
    if os.path.basename(file) == videoName:
        selectedVideo = file
        break

#open the video
cap = cv2.VideoCapture(selectedVideo)
#get the user entered frames from the video
frame1 = ""
frame2 = ""

while(cap.isOpened()):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()





displayGrayscale = raw_input("Display the grayscale representations of frames?(Y/N): ")
if displayGrayscale == "Y":
    #create our grayscale representations of these frames
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    #display these grayscale representations to the user
    cv2.imshow('Grayscale of Frame 1',gray1)
    cv2.imshow('Grayscale of Frame 2',gray2)
    hideGrayscale = raw_input("Press any key to continue and close grayscale images: ")
    if hideGrayscale != "":
      cv2.destroyAllWindows()
else:
    displayGrayscale = raw_input("Display the DELTA difference images?(Y/N): ")

