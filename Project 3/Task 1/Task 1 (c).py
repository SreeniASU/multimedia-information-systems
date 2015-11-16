import cv2
import numpy as np
import sys
import os

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
Applies 3 stage 2D Haar wavelet transform on each block, returning an 8x8
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
def dwt(block):
    # First dwt transform
    dwt = haar(block)
    # Second dwt transform
    dwt[:4,:4] = haar(dwt[:4,:4])
    # Third dwt transform
    dwt[:2,:2] = haar(dwt[:2,:2])
    return dwt

'''
video_blockdwt
Applies block-wise dwt to video and writes to .bwt file
- file_path - absolute path to video .mp4 file
- n - number of significant signals to write
Has side-effect of writing output to .bwt file
'''
def video_blockdwt(file_path, n):
    wavelet_ids = [
        'LL300', 'HL300', 'HL200', 'HL201', 'HL100', 'HL101', 'HL102', 'HL103',
        'LH300', 'HH300', 'HL210', 'HL211', 'HL110', 'HL111', 'HL112', 'HL113',
        'LH200', 'LH201', 'HH200', 'HH201', 'HL120', 'HL121', 'HL122', 'HL123',
        'LH210', 'LH211', 'HH210', 'HH211', 'HL130', 'HL131', 'HL132', 'HL133',
        'LH100', 'LH101', 'LH102', 'LH103', 'HH100', 'HH101', 'HH102', 'HH103',
        'LH110', 'LH111', 'LH112', 'LH113', 'HH110', 'HH111', 'HH112', 'HH113',
        'LH120', 'LH121', 'LH122', 'LH123', 'HH120', 'HH121', 'HH122', 'HH123',
        'LH130', 'LH131', 'LH132', 'LH133', 'HH130', 'HH131', 'HH132', 'HH133']
    video = cv2.VideoCapture(file_path)
    frameNum = 0
    outputFile = open(file_path.strip('.mp4') + '_blockdwt_' + str(n) + '.bwt', 'w')
    while video.isOpened():
        ret, frame = video.read()
        if ret:
            frameNum += 1
            print('Frame number: ' + str(frameNum))
            yFrameValues = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            for blockI in range(0, len(frame), 8):
                for blockJ in range(0, len(frame[blockI]), 8):
                    block = yFrameValues[blockI:blockI+8,blockJ:blockJ+8]
                    block_dwt = dwt(block)
                    indexes_of_significant_wavelets = np.argsort(np.absolute(block_dwt), axis=None)[::-1]
                    for i in range(n):
                        index = indexes_of_significant_wavelets[i]
                        value = block_dwt[index//8, index%8]
                        wavelet_comp_id = wavelet_ids[index]
                        outputFile.write('<' + str(frameNum) + ',(' + str(blockI) + ',' + str(blockJ) + '),' + wavelet_comp_id + ',' + str(value) + '>\n')
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
        print 'Usage: python Task1c.py ../path/to/file.mp4 4'
        exit()

    file_path = os.path.realpath(sys.argv[1])
    n = int(sys.argv[2])

    video_blockdwt(file_path, n)
