__author__ = 'Team 6'
import Utility as util
import cv2
import numpy as np
import time
from os import listdir
from os.path import isfile,join

freq_component_ids = [
    '00','01','02','03','04','05','06','07',
    '10','11','12','13','14','15','16','17',
    '20','21','22','23','24','25','26','27',
    '30','31','32','33','34','35','36','37',
    '40','41','42','43','44','45','46','47',
    '50','51','52','53','54','55','56','57',
    '60','61','62','63','64','65','66','67',
    '70','71','72','73','74','75','76','77',

]


# Naive implementation of DCT by directly using the formula
# Not very good with performance but sticking on to that as this is
# the direct implementation of the formula and easier to read
def FindDCT(input):
    DCT = np.zeros((8,8))
    # DCT should be applied on values from -128 to + 127 not from 0 to 255
    input = input - 128
    for i in range(0,8):
        for j in range(0,8):
            temp = 0.0
            for x in range(0,8):
                for y in range(0,8):
                    temp = temp +  np.cos(np.pi*i *(2*x+1)/16) * np.cos(np.pi*j *(2*y+1)/16) * input[x,y]
            if i== 0 and j == 0:
                temp = temp/8
            elif i == 0 or j==0:
                temp = temp/(4 *np.sqrt(2))
            else:
                temp = temp/4
            DCT[i][j] = temp
    return DCT


# A Faster implementation of DCT
# Reference :- http://www.whydomath.org/node/wavlets/dct.html
U =  np.array([[1/np.sqrt(2), 1/np.sqrt(2),1/np.sqrt(2), 1/np.sqrt(2),1/np.sqrt(2), 1/np.sqrt(2),1/np.sqrt(2), 1/np.sqrt(2)],
                  [np.cos(np.pi/16),np.cos(3*np.pi/16),np.cos(5*np.pi/16),np.cos(7*np.pi/16),np.cos(9*np.pi/16),np.cos(11*np.pi/16),np.cos(13*np.pi/16),np.cos(15*np.pi/16)],
                  [np.cos(2*np.pi/16),np.cos(6*np.pi/16),np.cos(10*np.pi/16),np.cos(14*np.pi/16),np.cos(18*np.pi/16),np.cos(22*np.pi/16),np.cos(26*np.pi/16),np.cos(30*np.pi/16)],
                  [np.cos(3*np.pi/16),np.cos(9*np.pi/16),np.cos(15*np.pi/16),np.cos(21*np.pi/16),np.cos(27*np.pi/16),np.cos(33*np.pi/16),np.cos(39*np.pi/16),np.cos(45*np.pi/16)],
                  [np.cos(4*np.pi/16),np.cos(12*np.pi/16),np.cos(20*np.pi/16),np.cos(28*np.pi/16),np.cos(36*np.pi/16),np.cos(44*np.pi/16),np.cos(52*np.pi/16),np.cos(60*np.pi/16)],
                  [np.cos(5*np.pi/16),np.cos(15*np.pi/16),np.cos(25*np.pi/16),np.cos(35*np.pi/16),np.cos(45*np.pi/16),np.cos(55*np.pi/16),np.cos(65*np.pi/16),np.cos(75*np.pi/16)],
                  [np.cos(6*np.pi/16),np.cos(18*np.pi/16),np.cos(30*np.pi/16),np.cos(42*np.pi/16),np.cos(54*np.pi/16),np.cos(66*np.pi/16),np.cos(78*np.pi/16),np.cos(90*np.pi/16)],
                  [np.cos(7*np.pi/16),np.cos(21*np.pi/16),np.cos(35*np.pi/16),np.cos(49*np.pi/16),np.cos(63*np.pi/16),np.cos(77*np.pi/16),np.cos(91*np.pi/16),np.cos(105*np.pi/16)]])

def FindDCTFast(input):
    input = input - 128
    C = np.dot(U/2,input)
    return np.dot(C, np.transpose(U/2))


def FindDiscreteCosineTransform(videoForProcessing,n):
    print("Splitting the video into frames")
    video = cv2.VideoCapture(videoForProcessing)
    ret, frame = video.read()
    width = int(video.get(3))
    height = int(video.get(4))
    outputFile = open(videoForProcessing.strip('.mp4') + '_blockdct_' + str(n) + '.bct', 'w')

    #print("Width is " + str(video.get(3)))
    #print("Height is" + str(video.get(4)))
    frameNum = 0
    while(video.isOpened()):
        ret, frame = video.read()
        if ret:
            frameNum +=1
            yFrameValues = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            for blockI in range(0,len(frame), 8):
                for blockJ in range(0, len(frame[blockI]), 8):
                    block = yFrameValues[blockI:blockI+8,blockJ:blockJ+8]
                    #FindDCT method is really slow
                    #If you want to compute DCT faster please use FindDCTFast method
                    transform = FindDCT(block)
                    significant_cosine_components = np.argsort(np.absolute(transform), axis = None)[::-1]
                    for i in range(n):
                        index = significant_cosine_components[i]
                        value = transform[index//8, index%8]
                        freq_comp_id = freq_component_ids[index]
                        outputFile.write('<' + str(frameNum) + ',(' + str(blockI) + ',' + str(blockJ) + '),' + freq_comp_id + ',' + str(value) + '>\n')
            break
        else:
            break
    outputFile.close()

if __name__ == '__main__':
    # Directory in which all the video files are pesent
    rootDir = util.safegetdirectory()
    #rootDir = "//Users//sreeni//Videos/inputvideos"
    # Get all the files from the root directory
    allFiles = [f for f in listdir(rootDir) if isfile(join(rootDir,f))]
    print(allFiles)
    n = input("Enter the number of cosine transform components")
    #Get the video for processing
    videoName = util.getvideofile(allFiles)
    videoForProcessing = join(rootDir, videoName)

    #print(videoForProcessing)
    FindDiscreteCosineTransform(videoForProcessing,n)
