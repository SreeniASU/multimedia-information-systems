import cv2
import numpy as np
import sys
import utility as util
from os import listdir, path

'''
harr(block)
Applies one stage of 2D Haar wavelet transform on the given block
'''
def haar(block):
    vertical_lowpass = (block[:, ::2] + block[:, 1::2])/2.0
    vertical_highpass = (block[:, ::2] - block[:, 1::2])/2.0
    vertical_dwt = np.hstack((vertical_lowpass, vertical_highpass))

    horizontal_lowpass = (vertical_dwt[::2] + vertical_dwt[1::2])/2.0
    horizontal_highpass = (vertical_dwt[::2] - vertical_dwt[1::2])/2.0
    dwt = np.vstack((horizontal_lowpass, horizontal_highpass))
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
    dwt[:4, :4] = haar(dwt[:4, :4])
    # Third dwt transform
    dwt[:2, :2] = haar(dwt[:2, :2])
    return dwt

def video_blockdwt(frame_data, n):
    '''
    video_blockdwt
    Applies block-wise dwt to video and writes to .bwt file
    - file_path - absolute path to video .mp4 file
    - n - number of significant signals to write
    Has side-effect of writing output to .bwt file
    '''
    frame_num = 0
    result = list()

    for frame in frame_data:
        frame_num += 1
        print 'Frame number: ' + str(frame_num)
        for block_x in range(0, len(frame), 8):
            for block_y in range(0, len(frame[block_x]), 8):
                block = frame[block_x:block_x+8, block_y:block_y+8]
                block_dwt = dwt(block)
                indexes_of_significant_wavelets = np.argsort(np.absolute(block_dwt), axis=None)[::-1]
                for i in range(n):
                    index = indexes_of_significant_wavelets[i]
                    wavelet_x = index//8
                    wavelet_y = index%8
                    result.append({
                        'frame_num': frame_num,
                        'block_coords': (block_x, block_y),
                        'key': (wavelet_x, wavelet_y),
                        'val': block_dwt[wavelet_x, wavelet_y]
                    })

    return result

'''
Main Method
Given a video file `video_filename.mp4` and an `n` value, will output a text file video_filename_blockdwt_n.bwt in the same directory.
Pass the parameters in via command line parameters.
'''
if __name__ == '__main__':
    if len(sys.argv) == 1:
        root_dir = util.safeGetDirectory()
        all_files = [f for f in listdir(root_dir) if path.isfile(path.join(root_dir, f))]
        input_file = util.getVideoFile(all_files)
        n = util.getNValue()
        filename = path.join(root_dir, input_file)
    elif len(sys.argv) == 3:
        filename = path.realpath(sys.argv[2])
        n = int(sys.argv[1])
    else:
        print 'Usage: python block_dwt.py 6 ../path/to/file.mp4'
        exit()

    # Read the video data
    video = cv2.VideoCapture(filename)
    frame_data = util.getContent(video)

    # Calculate the wavelet components of each frameblock
    significant_wavelets = video_blockdwt(frame_data, n)

    # Write the data to the file
    output_filename = filename.replace('.mp4', '_blockdwt_' + str(n) + '.bwt')
    util.save_to_file(significant_wavelets, output_filename)
