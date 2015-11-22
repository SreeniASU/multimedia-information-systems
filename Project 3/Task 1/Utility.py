__author__ = 'Team 6'

#Class which contains the util methods

def showfiles(files):
    print('======= List of Files =======')
    print('\n'.join(str(p) for p in files))
    print('===================================')
    return

def safeGetDirectory():
    while(1):
        try:
            rootdirectory = raw_input("Enter the location of video files")
            validate = raw_input("Directory set to: " + rootdirectory + " is this okay? Y/N    ")
            if(validate == 'Y' or validate == 'y'):
                return rootdirectory
        except:
            print("Error getting directory")




def getVideoFile(files):
    showfiles(files)
    while 1:
        try:
            fileName = raw_input("Enter the name of the file you would like to process: \n")
            validate = raw_input("File set to: " + fileName + " is this okay? Y/N:   ")
            if validate == 'y' or validate == 'Y':
                if fileName in files:
                    return fileName
        except:
            print("File not found, please choose another file.")

def writeToFile(outputFile,content):
    rows = len(content)
    for i in range(rows):
        outputFile.write(content[i])
    return
