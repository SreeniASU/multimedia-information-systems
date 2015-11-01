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
    print("2. Predictive encoding with Predictor A")
    print("3. Predictive encoding with Predictor B")
    print("4. Predictive encoding with Predictor C")
    print("5. Predictive encoding with a1 * A + a2 * B + a3 * C")
    return (raw_input("Select an option :"))

def getPixelRegion():
    return input("Enter the origin of the 10x10 pixel region: ")
