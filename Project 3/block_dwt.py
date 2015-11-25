import cv2
import numpy as np
import sys
import utility as util
from os import listdir, path


'''
Stores the indices of the DWT matrix and the order in which the
data needs to be read from the matrix
'''
zigzag = [(0,0),(0,1),(1,0),(2,0),(1,1),(0,2),(0,3),(1,2),
          (2,1),(3,0),(4,0),(3,1),(2,2),(1,3),(0,4),(0,5),
          (1,4),(2,3),(3,2),(4,1),(5,0),(6,0),(5,1),(4,2),
          (3,3),(2,4),(1,5),(0,6),(0,7),(1,6),(2,5),(3,4),
          (4,3),(5,2),(6,1),(7,0),(7,1),(6,2),(5,3),(4,4),
          (3,5),(2,6),(1,7),(2,7),(3,6),(4,5),(5,4),(6,3),
          (7,2),(7,3),(6,4),(5,5),(4,6),(3,7),(4,7),(5,6),
          (6,5),(7,4),(7,5),(6,6),(5,7),(6,7),(7,6),(7,7)]

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
                for i in range(n):
                    result.append({
                        'frame_num': frame_num,
                        'block_coords': (block_x, block_y),
                        'key': zigzag[i],
                        'val': block_dwt[zigzag[i]]
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
        n = util.getConstant('n')
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
