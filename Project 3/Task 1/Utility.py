import numpy as np
import cv2
__author__ = 'Team 6'

#Class which contains the util methods

def showfiles(files):
    print('======= List of Files =======')
    print('\n'.join(str(p) for p in files))
    print('===================================')
    return

def safeGetDirectory():
    while(1):
        try:
            rootdirectory = raw_input("Enter the location of video files")
            validate = raw_input("Directory set to: " + rootdirectory + " is this okay? Y/N    ")
            if(validate == 'Y' or validate == 'y'):
                return rootdirectory
        except:
            print("Error getting directory")

def getNValue():
      while 1:
        try:
            option = input('Please enter an m value: ')
            if option < 1:
                print(str(option) + ' is not a valid selection. Please make a different selection.\n')
            else:
                return option
        except:
            print(str(option) + ' is not a valid input. Please try again.\n')

def getContent(video):
    frameData = list()
    while(video.isOpened()):
        ret, frame = video.read()
        if ret:
            yFrameValues = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frameData.append(yFrameValues)
        else:
            break
    # Possibly revisit to add max and min here
    return frameData

def save_to_file(data_values, filename):
    output_file = open(filename, 'w')
    output_format = '< {frame_num}, {block_coords}, {key}, {val} >\n'
    for item in data_values:
        output_file.write(output_format.format(**item))
    output_file.close()


def getVideoFile(files):
    showfiles(files)
    while 1:
        try:
            fileName = raw_input("Enter the name of the file you would like to process: \n")
            validate = raw_input("File set to: " + fileName + " is this okay? Y/N:   ")
            if validate == 'y' or validate == 'Y':
                if fileName in files:
                    return fileName
        except:
            print("File not found, please choose another file.")

def writeToFile(outputFile,content):
    rows = len(content)
    for i in range(rows):
        outputFile.write(content[i])
    return
