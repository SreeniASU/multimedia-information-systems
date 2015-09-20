__author__ = 'Team 6'
# CSE 408/598 Project 1- Part 2
#======================================
#Description:
#Implement a program that will allow the user to select
#- A color space
#- Three colors c0, c1, c2
#- Number of bits of storage
#given these
#- creates a colormap which maps each value in range -1 to +1 along the continuous path from c0 to c2 through c1 in 3D space.
#- c0 will be mapped to -1, c1 will be mapped to 0 and c2 will be mapped to +1
#======================================
import cv2
import numpy as np
import math

from colormap2image import colormap2image

# Class which handles colormap creation
def createColorMap(c0, c1, c2, numberOfBits):
    # Creates the colormap based on the user inputs
    # The algorithm for the method goes like this
    # ==================================================
    # numberOfColors - Number of colors in the colormap which is 2^number of bits entered by the user
    # numberOfSplits - Number of intervals in which C0-C1 or C1-C2 is split, which is numberOfColors/2
    # eg if numberofBits is 3, total number of colors in the color map is 8 and C0-C1 will be split into 4 and C1-C2 will
    # be split into 4
    # C0 + (C1-C0)*1/numberOfSplits will give first color next to C0
    # C0 + (C1-C0)*2/numberOfSplits will give second color next to C0 and so on
    # If C0 = (1,1,1), C1 = (3,3,3) C2 = (5,5,5) and numberOfBits = 2
    # The colormap will have colors (1,1,1), (2,2,2), (3,3,3), (5,5,5) so that
    # (1,1,1) can be mapped to [-1, -0.5)
    # (2,2,2) can be mapped to [-0.5,0)
    # (3,3,3) can be mapped to [0, +0.5]
    # (5,5,5) can be mapped to [+0.5,+1]
    # ===============================================

    numberOfColors = int(math.pow(2, numberOfBits))
    print('A colormap with '+ str(numberOfColors) + ' colors will be created \n')
    colors  = [];
    diff1 = np.subtract(c1, c0)
    numberOfSplits = int(numberOfColors/2);
    for i in xrange(0,numberOfSplits):
        colors.append(tuple(np.add( c0, tuple([int(math.ceil(float(i)/float(numberOfSplits)*float(x))) for x in diff1]))))
    diff2 = np.subtract(c2, c1)
    for i in xrange(0,numberOfSplits-1):
        colors.append(tuple(np.add( c1, tuple([int(math.ceil(float(i)/float(numberOfSplits)*float(x))) for x in diff2]))))
    colors.append(c2)
    return colors

if __name__ == '__main__':
    # Asks the user for the color space to be used
    print('Available color spaces  \n')
    print('*****************************\n')
    print(' 1. RGB \n 2. XYZ \n 3. Lab \n 4. Luv \n 5.YCrCb \n 6. HLS \n 7. HSV \n')
    colorSpace = int( input('Enter colorspace (1-7) to be used: '))
    while colorSpace < 1  or colorSpace >7:
        colorSpace = input('Invalid colorspace chosen, enter one between (1-7): ')

    xmin = 0
    xmax = 255
    ymin = 0
    ymax = 255
    zmin = 0
    zmax = 255
    # Maximum and minimum range for R, G and B channels
    if colorSpace == 1:
        xmin = 0
        xmax = 255
        ymin = 0
        ymax = 255
        zmin = 0
        zmax = 255
    # Maximum and minimumum range for X, Y and Z channels. This needs to be verified once again
    elif colorSpace == 2:
        xmin = 0
        xmax = 242
        ymin = 0
        ymax = 255
        zmin = 0
        zmax = 277
    # Maximuum and minimum range for L*a*b* channels
    elif colorSpace == 3:
        xmin = 1
        xmax = 255
        ymin = 1
        ymax = 255
        zmin = 1
        zmax = 255
    # Maximum and minimum range for Luv channels
    elif colorSpace == 4:
        xmin = 0
        xmax = 255
        ymin = 0
        ymax = 255
        zmin = 0
        zmax = 255
    # Maximum and minimum range for YCrCb channels
    elif colorSpace == 5:
        xmin = 0
        xmax = 255
        ymin = 0
        ymax = 255
        zmin = 0
        zmax = 255
    # Maximum and minumum range for HLS channels(Need to be verified)
    elif colorSpace == 6:
        xmin = 0
        xmax = 255
        ymin = 0
        ymax = 255
        zmin = 0
        zmax = 255
    # Maximum and minumum range for HSV channels
    elif colorSpace == 7:
        xmin = 0
        xmax = 180
        ymin = 0
        ymax = 255
        zmin = 0
        zmax = 255

    c0 = input('Enter value of C0, the format should be (' + str(xmin) + '-' + str(xmax) + ','
            + str(ymin) + '-' + str(ymax) + ',' + str(zmin) + '-' + str(zmax) + '): ' )
    c1 = input('Enter value of C1, the format should be (' + str(xmin) + '-' + str(xmax) + ','
            + str(ymin) + '-' + str(ymax) + ',' + str(zmin) + '-' + str(zmax) + '): ' )
    c2 = input('Enter value of C2, the format should be (' + str(xmin) + '-' + str(xmax) + ','
            + str(ymin) + '-' + str(ymax) + ',' + str(zmin) + '-' + str(zmax) + '): ' )

    # Asks the user for the number of bits
    numberOfBits = input('Enter number of bits (from 2 to 8): ')

    colorSpaceMap = { 1: 'RGB', 2: 'XYZ', 3: 'Lab', 4: 'Luv', 5: 'YCrCb', 6: 'HLS', 7: 'HSV' }
    colorSpace = colorSpaceMap[colorSpace]

    colorMap = createColorMap(c0, c1, c2, numberOfBits)

    print('Writing the colormap to text file')
    file = open('colormaptextfile.txt','w')
    file.write(str(colorMap))
    file.close()

    print('Printing the colormap to a jpg file')
    im_color = colormap2image(colorMap, colorSpace)
    cv2.imwrite('colormap.jpg', im_color)
    cv2.imshow("Pseudo Colored Image", im_color)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
