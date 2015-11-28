#!/usr/bin/env python
'''
Quantizes each block-frame of a video
Writes block-level quantized data in the following format to a file:
< FrameNumber, (X coordinate, Y coordinate) , Y Channel Value, Number Of Occurances >
Also displays a histogram with n bins and writes the histogram as a png
'''
import sys
import math
import numpy as np
import cv2
import matplotlib.pyplot as plt
import utility as util
from os import listdir, path

def quantize_block(block, bins, frame_num, block_x, block_y):
    '''
    Quantizes a block using the number of bins
    Returns a formatted string for output to a file which details the information in the format:
    < FrameNumber, (X coordinate, Y coordinate) , Y Channel Value, Number Of Occurances >
    '''
    min_value = np.amin(block)
    max_value = np.amax(block)
    samples, bin_size = np.linspace(min_value, max_value, bins, endpoint=False, retstep=True)
    samples += 0.5*bin_size
    samples = map((lambda v: round(v, 7)), samples)
    #dictionary to contain how many times a value occurs
    frame_occurances = dict.fromkeys(samples, 0)

    for val in np.nditer(block):
        if bin_size == 0:
            quantized_value = min_value
        else:
            quanta = math.floor((val - min_value) / bin_size) + 0.5
            quantized_value = min_value + quanta * bin_size

        if quantized_value >= max_value:
            quantized_value = min_value + (bins - 0.5)*bin_size

        quantized_value = round(quantized_value, 7)
        frame_occurances[quantized_value] += 1

    result = list()

    if min_value == max_value:
        max_value += 1

    block_hist = cv2.calcHist([block.astype(np.uint8)],[0],None,[bins],[min_value,max_value]) #We could do our local min/max here but lets keep the range (0,256) the same for comparison reasons

    for key in frame_occurances:
        result.append({
            'frame_num': frame_num,
            'block_coords': (block_x, block_y),
            'key': key,
            'val': frame_occurances[key]
        })

    return result, block_hist #only 1 histogram per block, dont save to dict for each value in block, but return for the whole block and construct dict to access for compare

def quantize(frame_data, n):
    '''
    Runs quantization on an entire frame by breaking down into
    bins and calling `quantize_block`
    '''
    print 'Running quantization with ' + str(n) + ' bins...'

    result = list()
    frame_block_dict = {}   #stores block dictionary which contains histogram data for blocks
    frame_num = 0

    #for each entry in frame_data
    for frame in frame_data:
        frame_num += 1
        print 'Processing regions of frame: ' + str(frame_num)
        for block_x in range(0, len(frame), 8):
            block_hist_dict = {}    #stores histogram data for blocks of a frame
            for block_y in range(0, len(frame[block_x]), 8):
                block = frame[block_x:block_x+8, block_y:block_y+8]
                block_dict,block_hist = quantize_block(block, n, frame_num, block_x, block_y)
                block_hist_dict[block_x,block_y] = block_hist
                result.extend(block_dict)

            frame_block_dict[frame_num] = block_hist_dict

    return result, frame_block_dict

def display_histogram(quantized_values, n, from_file=False, image_filename=''):
    print 'Creating histogram.'
    histogram = dict()

    if from_file:
        # TODO: implement readfile function from file to quantized_values
        quantized_values = util.readFile(quantized_values)

    for item in quantized_values:
        if item['key'] not in histogram:
            histogram[item['key']] = 0

        histogram[item['key']] += item['val']  #increment the value at the key by the given

    plt.hist(histogram.keys(), bins=n, weights=histogram.values())

    if len(image_filename) > 0:
        print 'Saving histogram image to ' + image_filename
        plt.savefig(image_filename)

    print 'Press any key or click to continue.'
    plt.show()


'''
Main Method
Prompts the user for an input file, a quantization option selection, and an m value.
Uses these values to quantize the input files error into 2^m uniform bins.
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
        print 'Usage: python block_quantize.py 6 ../path/to/file.mp4'
        exit()


    # Read video data
    video = cv2.VideoCapture(filename)
    frame_data = util.getContent(video)

    # Quantize the blocks of the video
    quantized_values, frame_block_list = quantize(frame_data, n)

    # Write the data to the file
    output_filename = filename.replace('.mp4', '_hist_' + str(n) + '.hst')
    util.save_to_file(quantized_values, output_filename)

    # Display histogram of quantized regions
    image_filename = output_filename.replace('.hst', '.png')
    display_histogram(quantized_values, n, image_filename=image_filename)
