#Checklist
"""
	- Encode the data and write it to another file(DONE), along with the dictionary(UNDONE)
	- Dictionary bit length for LZW
	- Output LZW data as a string, not as a list(maybe)
	- Figure out why LZW is not working 100%

	FOR TESTING: 
	- Decode the data contained on the encoded file
"""

from os import listdir
from os.path import isfile,join
import Utility as util
import shannon_fano as sf
import lzw
import arithmetic_coding as ac


def LZW(file_content):
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

	writeToFile(3,1,encoded_string)

	# print("Encoded string: " + ''.join(encoded_string))

	print "Decoding data..."
	decoded_string = lzw.lzwDecoder(encoded_string,dictionary)
	print "Decoding finished!\n"

	writeToFile(3,0,decoded_string)

	# print("Decoded string: " + decoded_string)

	# if (string == decoded_string):
		# print "Decoding was successful!"
	
def shannonFano(file_content):
	frequency = sf.stringFrequencyValues(file_content)

	sf.selectionSort(frequency) #sorts the array based on the frequency...
	frequency.reverse() #...then reverses it so that the biggest values come first

	encodedTree = sf.shannonFanoEncoder(frequency)

	sf.setCodes(encodedTree,"")

	print "Creating dictionary...\n "
	dictionary = sf.createDictionary(encodedTree,frequency)

	print "Encoding data...\n"
	encodedString = sf.encodeString(file_content,dictionary)

	writeToFile(2,1,encodedString)

	decodedString = sf.decodeString(encodedString,dictionary)

	writeToFile(2,0,decodedString)

	print "Finished!\n"

	if (decodedString == file_content):
		print "Decoding was successful!"

def arithmeticCoding(file_content):
	file_content = ac.updateString(file_content)

	print "Creating dictionary...\n"
	dictionary = ac.createDictionary(file_content)

	print "Calculating the frequency interval for the given data...\n"
	#first, the final frequency interval is calculated for the given string
	frequency_interval = ac.frequencyInterval(file_content,dictionary)

	print "Encoding data...\n"
	code = ac.arithmetic_encode(frequency_interval)

	writeToFile(4,1,code)

	print "Decoding data...\n"
	decoded_string = ac.arithmetic_decode(code,dictionary)

	writeToFile(4,0,decoded_string)

	print "Finished!\n"

def writeToFile(option,type,data):
	#writes encoded data to file
	# print str(data)

	if (type == 1):
		print "Outputing data to file...\n"

		output_file = open('Data/X_Y_' + str(option) + '.tpc','w')
		output_file.write(str(data))
	elif (type == 0):
		print "Outputing decoded data to file...\n"
		output_file = open('Data/output_test_decoded.tpc','w')
		output_file.write(str(data))
	
	if (type == 1 or type == 2):
		output_file.close()

#------------------------------------------------------------------------------------------------------------------


rootDir = 'C:\Users\Crispino\Documents\GitHub\multimedia-information-systems\Project 2\Part 4\Data'#util.safeGetDirectory()
# allFiles = [f for f in listdir(rootDir) if isfile(join(rootDir,f))]
inputFileName =  'test.tpc'#util.getVideoFile(allFiles)

inputFilePath = rootDir + "/" + inputFileName

inputFile = open(inputFilePath,'r')

fileContent = inputFile.read()

codingType = util.selectCodingOption()

if (codingType == 1):
	#no coding
	writeToFile(1,1,fileContent)
elif (codingType == 2):
	shannonFano(fileContent)
elif (codingType == 3):
	LZW(fileContent)
elif (codingType == 4):
	arithmeticCoding(fileContent)