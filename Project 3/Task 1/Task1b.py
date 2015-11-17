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



def FindDCT(frame):
    imf = np.float32(frame)/255
    dst = cv2.dct(imf)
    return np.uint8(dst)*255.0


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




