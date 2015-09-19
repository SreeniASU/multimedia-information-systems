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

import colors2image as c2i

# Class which handles colormap creation
class ColorMapCreator:
    # Asks the user for the color space to be used
    def getColorSpace(self):
        print('Available color spaces  \n')
        print('*****************************\n')
        print(' 1. RGB \n 2. XYZ \n 3. Lab \n 4. Luv \n 5.YCrCb \n 6. HLS \n 7. HSV \n')
        self.colorSpace = input('Enter colorspace (1-7) to be used: ')

    # Asks the user for the three color instances from the color space
    # c0,c1,c2 will be stored as tuples
    def getColorInstance(self):
        self.c0 = input('Enter value for C0, the format should be (X,Y,Z): ')
        self.c1 = input('Enter value for C1, the format should be (X,Y,Z): ')
        self.c2 = input('Enter value for C2, the format should be (X,Y,Z): ')

    # Asks the user for the number of bits
    def getNumberOfBits(self):
        self.numberOfBits = input('Enter number of bits (from 2 to 8): ')

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

    def GetColorMap(self):
        numberOfColors = int(math.pow(2, self.numberOfBits))
        print('A colormap with '+ str(numberOfColors) + ' colors will be created \n')
        colors  = [];
        diff1 = np.subtract(self.c1 ,self.c0)
        numberOfSplits = int(numberOfColors/2);
        for i in xrange(0,numberOfSplits):
            colors.append(tuple(np.add( self.c0, tuple([int(math.ceil(float(i)/float(numberOfSplits)*float(x))) for x in diff1]))))
        diff2 = np.subtract(self.c2, self.c1)
        for i in xrange(0,numberOfSplits-1):
            colors.append(tuple(np.add( self.c1, tuple([int(math.ceil(float(i)/float(numberOfSplits)*float(x))) for x in diff2]))))
        colors.append(self.c2)
        return colors

    def __init__(self):
        self.getColorSpace()
        self.getColorInstance()
        self.getNumberOfBits()

colorMapCreatorObj = ColorMapCreator()
colorMap = colorMapCreatorObj.GetColorMap()

print('Writing the colormap to text file')
file = open('colormaptextfile.txt','w')
file.write(str(colorMap))
file.close()

print('Printing the colormap to a jpg file')
c2i.colors2image(colorMap, colorMapCreatorObj.colorSpace)









