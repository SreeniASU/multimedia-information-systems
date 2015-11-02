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

def showFiles(files):
	print('======= List of Files =======')
	print('\n'.join(str(p) for p in files))
	print('===================================')
	return

def safeGetDirectory():
	while 1:
		try:
			rootDir = raw_input('Please enter the path where video files are located: ')
			validate = raw_input("Directory set to: " + rootDir + " is this okay? Y/N    ")
			if(validate == 'Y' or validate == 'y'):
				return rootDir
		except:
			log("Directory not found!")

def getVideoFile(files):
    showFiles(files)
    while 1:
        try:
            fileName = raw_input("Enter the name of the file you would like to process: \n")
            validate = raw_input("File set to: " + fileName + " is this okay? Y/N:   ")
            if validate == 'y' or validate == 'Y':
                if fileName in files:
                    return fileName
        except:
            log("File not found, please choose another file.")

def getEncodingOption():
    print("Available Encoding Options:")
    print("1. No PC")
    print("2. Predictive encoding with the predictor s[t-1]")
    print("3. Predictive encoding with the predictor (s[t-1]+s[t-2])/2")
    print("4. Predictive encoding with the predictor a1 * s[t-1] + a2 * s[t-2]")
    option = raw_input("Select an option: ")
    return option

def getPixelRegion():
    return input("Enter the origin of the 10x10 pixel region: ")

def goBack(x, y, go_back, width=10):
    if x == 0 and (y == 0 or y == 1):
        return x, y
    elif y - go_back < 0:
        return x - 1, y + width - go_back
    else:
        return x, y - go_back

def selectCodingOption():
    option = 0  #initialize variable

    while (option < 1 or option > 4):
        print "Select which encoding option you want: "
        print "1. No compression"
        print "2. Shannon-Fano coding"
        print "3. LZW coding"
        print "4. Arithmetic coding"
        
        option = int(raw_input())

        if (option < 1 or option > 4):
            print "Invalid input! Please select a valid option."

    return option
