import re
import numpy as np

# Utility function for converting initialization string to
# a matrix
def stringToMatrix(matrixString):
    lines = matrixString.strip().split('\n')
    result = []
    for line in lines:
        values = line.strip(' []').split(' ')
        i = 0
        while i < len(values):
            if (len(values[i]) == 0):
                values.pop(i)
            else:
                values[i] = int(values[i])
                i += 1

        result.append(values)

    return result

def parseFile(filepath):
    inputFile = open(filepath, 'r')
    frames = []
    initString = ""
    init = []
    initFlag = False
    frame = -1
    for line in inputFile.readlines():
        if line[0] == "{":
            initFlag = True
        elif initFlag :
            if line[0]== "}": #finds end of initial value
               initFlag = False
               init.append(stringToMatrix(initString))
               initString = ""
            else:
               initString += line     # adds all lines of initial value of a frame to init.
        else:
            result = re.match("<(?P<f>\d+),(?P<x>\d),(?P<y>\d),(?P<e>-?\d+(.*)?)\n", line)
            if result:
                f = int(result.group("f")) - 1
                x = int(result.group("x"))
                y = int(result.group("y"))
                if (re.match(".*e.*",result.group("e"))):
                    e = 0
                else:
                    e = float(result.group("e"))

                if (f > frame):
                    frames.append(np.empty([10,10]))
                    frame += 1
                
                frames[f][x][y] = e
    
    return init, np.array(frames)
