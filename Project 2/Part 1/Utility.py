

def log (message):
    print(message)

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
