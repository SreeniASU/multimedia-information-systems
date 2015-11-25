__author__ = 'Team 6'
import utility as util
import sys
import cv2
import numpy as np
import time
from os import listdir, path

zigzag = [(0,0),(0,1),(1,0),(2,0),(1,1),(0,2),(0,3),(1,2),
          (2,1),(3,0),(4,0),(3,1),(2,2),(1,3),(0,4),(0,5),
          (1,4),(2,3),(3,2),(4,1),(5,0),(6,0),(5,1),(4,2),
          (3,3),(2,4),(1,5),(0,6),(0,7),(1,6),(2,5),(3,4),
          (4,3),(5,2),(6,1),(7,0),(7,1),(6,2),(5,3),(4,4),
          (3,5),(2,6),(1,7),(2,7),(3,6),(4,5),(5,4),(6,3),
          (7,2),(7,3),(6,4),(5,5),(4,6),(3,7),(4,7),(5,6),
          (6,5),(7,4),(7,5),(6,6),(5,7),(6,7),(7,6),(7,7)]

# Naive implementation of DCT by directly using the formula
# Not very good with performance but sticking on to that as this is
# the direct implementation of the formula and easier to read
def FindDCT(input_data):
    DCT = np.zeros((8, 8))
    # DCT should be applied on values from -128 to + 127 not from 0 to 255
    input_data = input_data - 128
    for i in range(0, 8):
        for j in range(0, 8):
            temp = 0.0
            for x in range(0, 8):
                for y in range(0, 8):
                    temp = temp + np.cos(np.pi*i *(2*x+1)/16) * np.cos(np.pi*j *(2*y+1)/16) * input_data[x, y]
            if i == 0 and j == 0:
                temp = temp/8
            elif i == 0 or j == 0:
                temp = temp/(4 *np.sqrt(2))
            else:
                temp = temp/4
            DCT[i][j] = temp
    return DCT


# A Faster implementation of DCT
# Reference :- http://www.whydomath.org/node/wavlets/dct.html
U = np.array([[1/np.sqrt(2), 1/np.sqrt(2), 1/np.sqrt(2), 1/np.sqrt(2), 1/np.sqrt(2), 1/np.sqrt(2), 1/np.sqrt(2), 1/np.sqrt(2)],
              [np.cos(np.pi/16), np.cos(3*np.pi/16), np.cos(5*np.pi/16), np.cos(7*np.pi/16), np.cos(9*np.pi/16), np.cos(11*np.pi/16), np.cos(13*np.pi/16), np.cos(15*np.pi/16)],
              [np.cos(2*np.pi/16), np.cos(6*np.pi/16), np.cos(10*np.pi/16), np.cos(14*np.pi/16), np.cos(18*np.pi/16), np.cos(22*np.pi/16), np.cos(26*np.pi/16), np.cos(30*np.pi/16)],
              [np.cos(3*np.pi/16), np.cos(9*np.pi/16), np.cos(15*np.pi/16), np.cos(21*np.pi/16), np.cos(27*np.pi/16), np.cos(33*np.pi/16), np.cos(39*np.pi/16), np.cos(45*np.pi/16)],
              [np.cos(4*np.pi/16), np.cos(12*np.pi/16), np.cos(20*np.pi/16), np.cos(28*np.pi/16), np.cos(36*np.pi/16), np.cos(44*np.pi/16), np.cos(52*np.pi/16), np.cos(60*np.pi/16)],
              [np.cos(5*np.pi/16), np.cos(15*np.pi/16), np.cos(25*np.pi/16), np.cos(35*np.pi/16), np.cos(45*np.pi/16), np.cos(55*np.pi/16), np.cos(65*np.pi/16), np.cos(75*np.pi/16)],
              [np.cos(6*np.pi/16), np.cos(18*np.pi/16), np.cos(30*np.pi/16), np.cos(42*np.pi/16), np.cos(54*np.pi/16), np.cos(66*np.pi/16), np.cos(78*np.pi/16), np.cos(90*np.pi/16)],
              [np.cos(7*np.pi/16), np.cos(21*np.pi/16), np.cos(35*np.pi/16), np.cos(49*np.pi/16), np.cos(63*np.pi/16), np.cos(77*np.pi/16), np.cos(91*np.pi/16), np.cos(105*np.pi/16)]])

def FindDCTFast(input):
    input = input - 128
    C = np.dot(U/2, input)
    return np.dot(C, np.transpose(U/2))


def FindDiscreteCosineTransform(frame_data, n):
    '''
    Calculates the discrete cosign components of every frameblock
    '''

    frame_num = 0
    result = list()

    for frame in frame_data:
        frame_num += 1
        print 'Frame number: ' + str(frame_num)
        for block_x in range(0, len(frame), 8):
            for block_y in range(0, len(frame[block_x]), 8):
                block = frame[block_x:block_x+8, block_y:block_y+8]
                #FindDCT method is really slow
                #If you want to compute DCT faster please use FindDCTFast method
                transform = FindDCTFast(block)

                for i in range(n):
                    result.append({
                        'frame_num': frame_num,
                        'block_coords': (block_x, block_y),
                        'key': zigzag[i],
                        'val': transform[zigzag[i]]
                    })
    return result

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
        print 'Usage: python block_dct.py 6 ../path/to/file.mp4'
        exit()

    # Read the video data
    video = cv2.VideoCapture(filename)
    frame_data = util.getContent(video)

    # Calculate the significant components
    significant_components = FindDiscreteCosineTransform(frame_data, n)

    # Write the data to the file
    output_filename = filename.replace('.mp4', '_blockdct_' + str(n) + '.bct')
    util.save_to_file(significant_components, output_filename)
