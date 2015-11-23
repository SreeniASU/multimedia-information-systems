#!/usr/bin/env python
import numpy as np
import cv2
import sys
from os import listdir, path
import utility as util
from block_quantize import quantize, display_histogram

def diff_quantize(frame_data, n):
    diff_frame_data = np.diff(frame_data, axis=0)
    # Quantize the blocks of the video
    quantized_values = quantize(diff_frame_data, n)
    return quantized_values


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
        print 'Usage: python diff_quantize.py 6 ../path/to/file.mp4'
        exit()

    video = cv2.VideoCapture(filename)
    frame_data = util.getContent(video)

    # Quantize the blocks of the video
    quantized_values = diff_quantize(frame_data, n)

    # Write the data to the file
    output_filename = filename.replace('.mp4', '_diff_' + str(n) + '.dhc')
    util.save_to_file(quantized_values, output_filename)

    # Display histogram of quantized regions
    image_filename = output_filename.replace('.dhc', '.png')
    display_histogram(quantized_values, n, image_filename=image_filename)
