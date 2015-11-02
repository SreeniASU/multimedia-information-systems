#Checklist
"""
	- Encode the data and write it to another file(DONE), along with the dictionary(UNDONE)
	- Dictionary bit length for LZW
	- Output SNR and size of the encoded video
	- Output LZW data as a string, not as a list(maybe)
	- Figure out why LZW is not working 100%
	- Clear writeToFile 'type' argument
	FOR TESTING: 
	- Decode the data contained on the encoded file
"""

from os import listdir
from os.path import isfile,join
import Utility as util
import shannon_fano as sf
import lzw
import arithmetic_coding as ac


def LZW(file_content,outputFileName):
	string = fileContent

	print "Creating dictionary..."
	dictionary = lzw.createDictionary(string)
	print "Dictionary created!\n"

	# print ("Original string: " + string)

	print "Encoding data..."
	encoded_string = lzw.lzwEncoder(string,dictionary)
	print "Data encoded!\n"

	print "Updating encoded string to binary values..."
	encoded_string = lzw.updateEncodedString(encoded_string,dictionary)
	print "Values updated!\n"

	print "Updating dictionary values to binary values..."
	dictionary = lzw.updateDictionary(dictionary)
	print "Values updated!"

	fileSize = writeToFile(3,1,encoded_string,dictionary,outputFileName)

	# print("Encoded string: " + ''.join(encoded_string))

	#------------------------------------------------------------
	#Decoding part - Should not be on Part IV
	# encoded_file = open('X_Y_3','r')

	# dictionary = getDicionaryFromFile(encoded_file)

	print "Decoding data..."
	decoded_string = lzw.lzwDecoder(encoded_string,dictionary)
	print "Decoding finished!\n"

	writeToFile(3,0,decoded_string,None,outputFileName)

	print "Finished!\n"
	#------------------------------------------------------------
	# print("Decoded string: " + decoded_string)

	# if (string == decoded_string):
		# print "Decoding was successful!"

	return fileSize
	
def shannonFano(file_content,outputFileName):
	frequency = sf.stringFrequencyValues(file_content)

	sf.selectionSort(frequency) #sorts the array based on the frequency...
	frequency.reverse() #...then reverses it so that the biggest values come first

	encodedTree = sf.shannonFanoEncoder(frequency)

	sf.setCodes(encodedTree,"")

	print "Creating dictionary...\n "
	dictionary = sf.createDictionary(encodedTree,frequency)

	print "Encoding data...\n"
	encodedString = sf.encodeString(file_content,dictionary)

	fileSize = writeToFile(2,1,encodedString,dictionary,outputFileName)

	decodedString = sf.decodeString(encodedString,dictionary)

	writeToFile(2,0,decodedString,None,outputFileName)

	print "Finished!\n"

	if (decodedString == file_content):
		print "Decoding was successful!"

	return fileSize

def arithmeticCoding(file_content, outputFileName):
	file_content = ac.updateString(file_content)

	print "Creating dictionary...\n"
	dictionary = ac.createDictionary(file_content)

	print "Calculating the frequency interval for the given data...\n"
	#first, the final frequency interval is calculated for the given string
	frequency_interval = ac.frequencyInterval(file_content,dictionary)

	print "Encoding data...\n"
	code = ac.arithmetic_encode(frequency_interval)

	fileSize = writeToFile(4,1,code,dictionary,outputFileName)

	print "Decoding data...\n"
	decoded_string = ac.arithmetic_decode(code,dictionary)

	writeToFile(4,0,decoded_string,None,outputFileName)

	print "Finished!\n"

	return fileSize

def writeToFile(option,type,data,dictionary,outputFileName):
	#writes encoded data to file

	if (type == 1):
		print "Outputing data to file...\n"

		#--------------------------------------------------------
		#file name handling for output file
		outputFileName = outputFileName[:outputFileName.find('.')] + '_' + str(option) + outputFileName[outputFileName.find('.'):]
		output_file_path = 'Data/' + outputFileName
		output_file = open(output_file_path,'w')
		#--------------------------------------------------------

		output = ""
		if (dictionary):
			output = str(dictionary)
		output += str(data)
		output_file.write(output.encode('utf-8'))

	elif (type == 0):
		print "Outputing decoded data to file...\n"
		output_file = open('Data/output_test_decoded.tpc','w')
		output_file.write(str(data))
	
	if (type == 0 or type == 1):
		output_file.close()

	if (option == 1):
		fileSize = len(data)
	else:
		fileSize = len(data)/8
	print fileSize
	if (dictionary):
		fileSize += len(str(dictionary))
		print len(str(dictionary))

	return fileSize

def getDicionaryFromFile(encoded_file):
	#gets and file object as a pointer and extracts the dictionary from it
	pass
#------------------------------------------------------------------------------------------------------------------


rootDir = '/Users/jake/Projects/multimedia-information-systems/Project 2/Part 1/data'#util.safeGetDirectory()
allFiles = [f for f in listdir(rootDir) if isfile(join(rootDir,f))]
inputFileName =  util.getVideoFile(allFiles)

#reads the input file name to check if it contains either spacial or temporal predictive coding data
predictive_type = inputFileName[inputFileName.find('.') + 1:inputFileName.find('.') + 2]

inputFilePath = rootDir + "/" + inputFileName

inputFile = open(inputFilePath,'r')

fileContent = inputFile.read()
inputFileSize = len(fileContent)

codingType = util.selectCodingOption()

outputfileSize = 0
outputFileName = inputFileName[:inputFileName.find('.')] + '.' + predictive_type + 'pc'
if (codingType == 1):
	#no coding
	outputfileSize = writeToFile(1,1,fileContent,None,outputFileName)
elif (codingType == 2):
	outputfileSize = shannonFano(fileContent,outputFileName)
elif (codingType == 3):
	outputfileSize = LZW(fileContent,outputFileName)
elif (codingType == 4):
	outputfileSize = arithmeticCoding(fileContent,outputFileName)

#it calculates the file size as if each binary bigit had a size of 1-bit, simulating a real compression state.
print "Original video file size: " + str(inputFileSize) + " bytes"
print "Encoded video file size: " + str(outputfileSize) + " bytes"

# snr = 
