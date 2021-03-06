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

import os
from os import listdir
from os.path import isfile,join,basename
import Utility as util
import shannon_fano as sf
import lzw
import arithmetic_coding as ac
import ast
from decimal import *

getcontext().prec = 20000 #precision of the floating point numbers

def LZW(fileContent,outputFileName, rootDir):
	string = fileContent

	print "Creating dictionary..."
	dictionary = lzw.createDictionary(string)
	print "Dictionary created!\n"

	bitLength = input('Please enter a dictionary size(sufficient size is 256): ')

	print "Encoding data..."
	encoded_string = lzw.lzwEncoder(string,bitLength)
	print "Data encoded!\n"

	fileSize = writeToFile(3,1,encoded_string,None,os.path.join(rootDir, outputFileName))

	print "Finished!\n"

	return fileSize
	
def shannonFano(file_content,outputFileName, rootDir):
	frequency = sf.stringFrequencyValues(file_content)

	sf.selectionSort(frequency) #sorts the array based on the frequency...
	frequency.reverse() #...then reverses it so that the biggest values come first

	encodedTree = sf.shannonFanoEncoder(frequency)

	sf.setCodes(encodedTree,"")

	print "Creating dictionary...\n "
	dictionary = sf.createDictionary(encodedTree,frequency)

	print "Encoding data...\n"
	encodedString = sf.encodeString(file_content,dictionary)

	fileSize = writeToFile(2,1,encodedString,dictionary,os.path.join(rootDir, outputFileName))

	print "Finished!\n"

	return fileSize

def arithmeticCoding(file_content, outputFileName, rootDir):
	file_content = ac.updateString(file_content)

	print "Creating dictionary...\n"
	dictionary = ac.createDictionary(file_content)

	print "Calculating the frequency interval for the given data...\n"
	#first, the final frequency interval is calculated for the given string
	frequency_interval = ac.frequencyInterval(file_content,dictionary)

	print "Encoding data...\n"
	code = ac.arithmetic_encode(frequency_interval)

	fileSize = writeToFile(4,1,code,dictionary,os.path.join(rootDir, outputFileName))

	'''
	print "Decoding data...\n"
	decoded_string = ac.arithmetic_decode(code,dictionary)

	writeToFile(4,0,decoded_string,None,outputFileName)

	print "Finished!\n"
	'''

	return fileSize

def shannonFanoDecode(file_path):
	#------------------------------------------------------------
	#Decoding part - Should not be on Part IV

	print "Opening file..."
	with open(file_path,'r') as f:
 		content = f.read()

	if "tpv" in file_path:
		file_path = file_path.strip("_2.tpv") + ".tpq"
	elif "spv" in file_path:
		file_path = file_path.strip("_2.spv") + ".spq"


	start = content.find("{'")
	end = content.find("~$!*")

	string_dictionary = content[start:end]
	# content.replace(content[start:end],'')
	content = content[end + 4:]

	dictionary = ast.literal_eval(string_dictionary)

	print "Decoding data..."
	decoded_string = sf.decodeString(content,dictionary)
	print "Decoding finished!\n"

	fileSize = writeToFile(3,0,decoded_string,None,file_path)

	return file_path

def LZWDecode(file_path):
	#------------------------------------------------------------
	#Decoding part - Should not be on Part IV

	with open(file_path,'r') as f:
 		content = f.read()

	if "tpv" in file_path:
		file_path = file_path.strip("_3.tpv") + ".tpq"
	elif "spv" in file_path:
		file_path = file_path.strip("_3.spv") + ".spq"

	print "Decoding data..."
	bitLength = input('Please enter a dictionary size(sufficient size is 256): ')
	decoded_string = lzw.lzwDecoder(ast.literal_eval(content),bitLength)
	print "Decoding finished!\n"

	fileSize = writeToFile(3,0,decoded_string,None,file_path)

	return file_path

def writeToFile(option,type,data,dictionary,outputFileName):
	#writes encoded data to file

	if (type == 1):
		print "Outputing data to file...\n"

		#--------------------------------------------------------
		#file name handling for output file
		outputFileName = outputFileName[:outputFileName.find('.')] + '_' + str(option) + outputFileName[outputFileName.find('.'):]
		print(outputFileName)
		output_file = open(outputFileName,'w')
		#--------------------------------------------------------

		output = ""
		if (dictionary):
			output = str(dictionary) + '~$!*'
		output += str(data)
		output_file.write(output.encode('utf-8'))

	elif (type == 0):
		print "Outputing decoded data to file...\n"
		output_file = open(outputFileName,'w')
		output_file.write(str(data))
	
	if (type == 0 or type == 1):
		output_file.close()

	if (option == 1):
		fileSize = len(data)
	else:
		fileSize = len(data)/8

	if (dictionary):
		fileSize += len(str(dictionary))
		print len(str(dictionary))

	return fileSize

def arithmeticCodingDecode(file_path):
	#------------------------------------------------------------
	#Decoding part - Should not be on Part IV

	print "Opening file..."
	with open(file_path,'r') as f:
 		content = f.read()

	if "tpv" in file_path:
		file_path = file_path.strip("_4.tpv") + ".tpq"
	elif "spv" in file_path:
		file_path = file_path.strip("_4.spv") + ".spq"


	start = content.find("{'")
	end = content.find("~$!*")

	string_dictionary = content[start:end]
	content = content[end + 4:]

	string_dictionary = string_dictionary.replace("Decimal(","")
	string_dictionary = string_dictionary.replace(")","")

	dictionary = ast.literal_eval(string_dictionary)

	for symbol in dictionary:
		dictionary[symbol][0] = Decimal(dictionary[symbol][0])
		dictionary[symbol][1] = Decimal(dictionary[symbol][1])

	print dictionary

	print "Decoding data...\n"
	decoded_string = ac.arithmetic_decode(content,dictionary)

	writeToFile(4,0,decoded_string,None,outputFileName)

	fileSize = writeToFile(3,0,decoded_string,None,file_path)

	return file_path

def getDicionaryFromFile(encoded_file):
	#gets and file object as a pointer and extracts the dictionary from it
	pass
#------------------------------------------------------------------------------------------------------------------
def compress(inputFilePath, codingType, rootDir):
    inputFile = open(inputFilePath,'r')

    fileContent = inputFile.read()
    inputFileSize = len(fileContent)
    inputFileName =  basename(inputFilePath)
    predictive_type = inputFileName[inputFileName.find('.') + 1:inputFileName.find('.') + 2]


    outputfileSize = 0
    outputFileName = inputFileName[:inputFileName.find('.')] + '.' + predictive_type + 'pv'
    if (codingType == 1):
        outputfileSize = writeToFile(1,1,fileContent,None,outputFileName)
    elif (codingType == 2):
        outputfileSize = shannonFano(fileContent,outputFileName, rootDir)
    elif (codingType == 3):
        outputfileSize = LZW(fileContent,outputFileName, rootDir)
    elif (codingType == 4):
        outputfileSize = arithmeticCoding(fileContent,outputFileName, rootDir)

    #it calculates the file size as if each binary digit had a size of 1-bit, simulating a real compression state.
    print "Original video file size: " + str(inputFileSize) + " bytes"
    print "Encoded video file size: " + str(outputfileSize) + " bytes"
    return outputFileName


if __name__ == '__main__':
    rootDir = util.safeGetDirectory()
    allFiles = [f for f in listdir(rootDir) if isfile(join(rootDir,f))]
    inputFileName =  util.getVideoFile(allFiles)

    #reads the input file name to check if it contains either spacial or temporal predictive coding data

    inputFilePath = rootDir + "/" + inputFileName
    codingType = util.selectCodingOption()

    compress(inputFilePath, codingType, rootDir)
