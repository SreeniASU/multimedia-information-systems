#!/usr/bin/env python

import cv2
import numpy as np

def colormap2image(colormap, colorspace) :

    lut = colormap2lut(colormap)
    im_color = applyCustomColorMap(lut, colorspace)
    return im_color

def colormap2lut(colormap) :
    
    times = 256 / len(colormap)
    lut = np.zeros((256, 1, 3), dtype=np.uint8)
    for i in xrange(0, len(colormap)):
        for j in xrange(0, times):
            lut[times*i+j][0] = colormap[i]

    return lut

def applyCustomColorMap(lut, colorspace) :

    gradient = np.arange(256, dtype=np.uint8).reshape(256, 1)
    row = np.ones(256, dtype=np.uint8)
    grid = (gradient * row).reshape(256, 256, 1)
    depth = np.ones(3, dtype=np.uint8)

    im_color = cv2.LUT(grid * depth, lut)

    if colorspace == 'RGB':
        # Convert to BGR:
        cv2.mixChannels(im_color, im_color, [0, 2, 1, 1, 2, 0])
    elif colorspace == 'XYZ':
        im_color = cv2.cvtColor(im_color, cv2.cv.CV_XYZ2BGR)
    elif colorspace == 'Lab':
        im_color = cv2.cvtColor(im_color, cv2.cv.CV_Lab2BGR)
    elif colorspace == 'Luv':
        im_color = cv2.cvtColor(im_color, cv2.cv.CV_Luv2BGR)
    elif colorspace == 'YCrCb':
        im_color = cv2.cvtColor(im_color, cv2.cv.CV_YCrCb2BGR)
    elif colorspace == 'HLS': 
        im_color = cv2.cvtColor(im_color, cv2.cv.CV_HSV2BGR)
    elif colorspace == 'HSV': 
        im_color = cv2.cvtColor(im_color, cv2.cv.CV_HSV2BGR)

    return im_color


if __name__  == '__main__' :

    file = open('colormaptextfile.txt', 'r')
    colormap = eval(file.read())

    colors2image(colormap, 'RGB');
