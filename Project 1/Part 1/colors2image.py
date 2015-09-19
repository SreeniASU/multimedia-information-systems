#!/usr/bin/env python

import cv2
import numpy as np

def colors2image(colormap, colorspace) :

    lut = colormap2lut(colormap)
    im_color = applyCustomColorMap(lut, colorspace)
    cv2.imwrite('colormap.jpg', im_color)
    cv2.imshow("Pseudo Colored Image", im_color)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

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

    # Cases for different color schemes:
    # default RGB for now, so switch B and R:

    if colorspace == 'RGB':
        red = np.zeros((256, 256, 1), dtype=np.uint8)
        red = np.copy(im_color[:, :, 2])
        im_color[:, :, 2] = im_color[:, :, 0]
        im_color[:, :, 0] = red
    else if colorspace == 'XYZ': 
        im_color = cv2.cvtColor(im_color, cv2.CV_XYZ2BGR)
    else if colorspace == 'Lab': 
        im_color = cv2.cvtColor(im_color, cv2.CV_Lab2BGR)
    else if colorspace == 'Luv': 
        im_color = cv2.cvtColor(im_color, cv2.CV_Luv2BGR)
    else if colorspace == 'YCrCb': 
        im_color = cv2.cvtColor(im_color, cv2.CV_YCrCb2BGR)
    else if colorspace == 'HLS': 
        im_color = cv2.cvtColor(im_color, cv2.CV_HSV2BGR)
    else if colorspace == 'HSV': 
        im_color = cv2.cvtColor(im_color, cv2.CV_HSV2BGR)

    return im_color


if __name__  == '__main__' :

    file = open('colormaptextfile.txt', 'r')
    colormap = eval(file.read())

    colors2image(colormap, 'RGB');
