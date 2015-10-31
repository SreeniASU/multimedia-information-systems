__author__ = 'azfut_000'

import cv2
import os.path
import numpy as np
from os import listdir
from os.path import isfile,join
import Utility as util
import math


givenFileName = "path_2.tpc" #sample file name to break apart
option = int((givenFileName.split('_',1)[1]).strip(".tpc")) #gets number from filename
print(option)

rootDir =os.path.join("E:","downloadsSSD","multimedia-information-systems-master")#,"multimedia-information-systems-master","test","project1") # windows path
fileName = "2_4.tpc"
print fileName

# rootDir = os.path.join( "C:" , "Users", "azfut_000", "PycharmProjects","part2", )
filepath = rootDir + "/" + fileName

inputFile = open(filepath, 'r')
frames = np.ndarray
frameArray= []
init = ""
initFlag = False
count = 0
for line in inputFile.readlines():
    str = line[0]

    if str == "{":
        initFlag = True
    elif initFlag :
        if line[-2]== "}": #finds end of initial value
               initFlag = False
        else:
               init += line     # adds all lines of initial value of a frame to init.
    else:
        # frameArray+=
        tempStr =((line.strip(">")).strip("<")).strip("\n")
        # print tempStr
        # temp = tempStr.split(',')
        f,x,y,error = tempStr.split(',')#temp[0],tempStr[1]+temp[2],temp
        pos = x,y
        if count<10:
            # print line
            print pos
            # print(frameArray)
        count += 1



#
# flags = ""
#
# for f in frames:
#     image = cv2.imdecode(f, flags)
#
#
#     cv2.WriteFrame(writer, image)