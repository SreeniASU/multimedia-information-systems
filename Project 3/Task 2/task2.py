import cv2
import numpy as np
import sys
import os
# from os import listdir
from os.path import join

'''
harr(block)
Applies one stage of 2D Haar wavelet transform on the given block
'''
def haar(block):
    vertical_dwt = np.hstack(
        ( (block[:,::2] + block[:,1::2])/2.0,
          (block[:,::2] - block[:,1::2])/2.0 ) )
    dwt = np.vstack(
        ( (vertical_dwt[::2] + vertical_dwt[1::2])/2.0,
          (vertical_dwt[::2] - vertical_dwt[1::2])/2.0 ) )
    return dwt

'''
dwt(block)
Applies 3 stage 2D Haar wavelet transform on each frame, returning an 8x8
array of the following form:
---------------------------------
|LL3|HL3|HL2    |HL1            |
----+---|       |               |
|LH3|HH3|       |               |
--------+-------|               |
|LH2    |HH2    |               |
|       |       |               |
|       |       |               |
----------------+----------------
|LH1            |HH1            |
|               |               |
|               |               |
|               |               |
|               |               |
|               |               |
|               |               |
---------------------------------
'''
def dwt(block, blockSize):
    # First dwt transform
    dwt = haar(block)

    count = 1
    while blockSize%(2*count)==0 :  # if blocksize is divisible by 2, then run haar on prev divided by 2
        count+=1
        blockSize/=2
        dwt[:blockSize,:blockSize] = haar(dwt[:blockSize,:blockSize])

    return dwt

'''
video_blockdwt
Applies block-wise dwt to video and writes to .bwt file
- file_path - absolute path to video .mp4 file
- n - number of significant signals to write
Has side-effect of writing output to .bwt file
'''
def video_blockdwt(file_path, n):

    video = cv2.VideoCapture(file_path)
    frameNum = 0
    outputFile = open(file_path.strip('.mp4') + '_ramedwt_' + str(n) + '.fwt', 'w')
    while video.isOpened():
        ret, frame = video.read()
        if ret:
            len(frame)
            frameNum += 1
            print('Frame number: ' + str(frameNum))
            yFrameValues = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            totalX = len(frame) #64
            # totalY = len(frame[0])  # don't need unless we are given non-square frames

            customBlock = totalX # size of the frame
            # customBlock = 8 # 8 would be used in task 1 part c

            for blockI in range(0, len(frame), customBlock):
                for blockJ in range(0, len(frame[blockI]), customBlock):
                    block = yFrameValues[blockI:blockI+customBlock,blockJ:blockJ+customBlock]
                    block_dwt = dwt(block,customBlock) # pass the size of the frame
                    indexes_of_significant_wavelets = np.argsort(np.absolute(block_dwt), axis=None)[::-1]
                    for i in range(n):
                        index = indexes_of_significant_wavelets[i]
                        value = block_dwt[index//customBlock, index%customBlock]
                        # wavelet_comp_id = wavelet_ids[index]
                        wavelet_comp_id = str(blockI) +","+ str(blockJ)
                        outputFile.write('<' + str(frameNum) + ',(' + str(blockI) + ',' + str(blockJ) + '),' + wavelet_comp_id + ',' + str(value) + '>\n')

                        # f ramedwt m.fwt
        else:
            break
    return

'''
Main Method
Given a video file `video_filename.mp4` and an `n` value, will output a text file video_filename_blockdwt_n.bwt in the same directory.
Pass the parameters in via command line parameters.
'''
if __name__ == '__main__':
    if len(sys.argv) != 3:

        # videoForProcessing = "R2.mp4" # util.getVideoFile(allFiles)    # for my testing, can be removed before submission
        # video_blockdwt(videoForProcessing,5)
        print 'Usage: python Task1c.py ../path/to/file.mp4 4'
        exit()

    file_path = os.path.realpath(sys.argv[1])
    n = int(sys.argv[2])

    video_blockdwt(file_path, n)
