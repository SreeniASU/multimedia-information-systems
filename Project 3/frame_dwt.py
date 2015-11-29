import cv2
import numpy as np
import sys
from os import listdir
from os import path
from block_dwt import haar
import utility as util

'''
dwt(block)
Applies m stage 2D Haar wavelet transform on each frame, returning an 8x8
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
def frame_dwt(frame):
    # First dwt transform
    dwt = haar(frame)

    blockSize = len(frame)/2
    count = 1

    while blockSize%2==0 :  # if blocksize is divisible by 2, then run haar on prev divided by 2
        dwt[:blockSize, :blockSize] = haar(dwt[:blockSize, :blockSize])
        blockSize/=2

    return dwt

def create_zigzag(width, height):
    result = list()

    x = 0
    y = 0

    while x < width-1 or y < height-1:
        result.append((x,y))
        if y < height-1:
            y += 1
        else:
            x += 1

        while y > 0 and x < width-1:
            result.append((x,y))
            y -= 1
            x += 1

        result.append((x,y))
        if x < width-1:
            x += 1
        else:
            y += 1

        while x > 0 and y < height-1:
            result.append((x,y))
            x -= 1
            y += 1

    result.append((x,y))
    return result

'''
video_blockdwt
Applies block-wise dwt to video and writes to .bwt file
- file_path - absolute path to video .mp4 file
- m - number of significant signals to write
Has side-effect of writing output to .bwt file
'''
def video_framedwt(frame_data, m):

    frame_num = 0
    result = list()

    # TODO: Add check here that prevents abnormal video files

    for frame in frame_data:
        frame_num += 1
        print 'Frame number: ' + str(frame_num)

        frame_wavelets = frame_dwt(frame)
        zigzag = create_zigzag(len(frame), len(frame[0]))
        for i in range(m):
            result.append({
                'frame_num': frame_num,
                'key': zigzag[i],
                'val': frame_wavelets[zigzag[i]]
            })

    return result

'''
Main Method
Given a video file `video_filename.mp4` and an `m` value, will output a text file video_filename_blockdwt_n.bwt in the same directory.
Pass the parameters in via command line parameters.
'''
if __name__ == '__main__':
    if len(sys.argv) == 1:
        root_dir = util.safeGetDirectory()
        all_files = [f for f in listdir(root_dir) if path.isfile(path.join(root_dir, f))]
        input_file = util.getVideoFile(all_files)
        m = util.getConstant('m')
        filename = path.join(root_dir, input_file)
    elif len(sys.argv) == 3:
        filename = path.realpath(sys.argv[2])
        m = int(sys.argv[1])
    else:
        print 'Usage: python frame_dwt.py 6 ../path/to/file.mp4'
        exit()

    # Read the video data
    video = cv2.VideoCapture(filename)
    frame_data = util.getContent(video)

    # Calculate the wavelet components of each frameblock
    significant_wavelets = video_framedwt(frame_data, m)

    # Write the data to the file
    output_filename = filename.replace('.mp4', '_framedwt_' + str(m) + '.fwt')
    util.save_to_file(significant_wavelets, output_filename)
