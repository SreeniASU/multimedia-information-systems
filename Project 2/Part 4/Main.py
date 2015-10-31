#Checklist
"""
	- Ask the user to choose which encoding option will be used
	- Encode the data and write it to another file, along with the dictionary

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
	# print 'string: ' + string

	# print("Encoded string: " + ''.join(encoded_string))

	print "Decoding data..."
	decoded_string = lzw.lzwDecoder(encoded_string,dictionary)
	print "Decoding finished!\n"

	# print("Decoded string: " + decoded_string)

	# if (string == decoded_string):
		# print "Decoding was successful!"
	
def shanonFano(file_content):
	frequency = sf.stringFrequencyValues(file_content)

	sf.selectionSort(frequency) #sorts the array based on the frequency...
	frequency.reverse() #...then reverses it so that the biggest values come first

	encodedTree = sf.shannonFanoEncoder(frequency)

	sf.setCodes(encodedTree,"")

	dictionary = sf.createDictionary(encodedTree,frequency)

	encodedString = sf.encodeString(file_content,dictionary)

	print "Outputing encoded data to file..."
	output_file_encoded = open('Data/output_test_encoded.tpc','w')
	output_file_encoded.write(str(encodedString))
	print "Finished!\n"

	decodedString = sf.decodeString(encodedString,dictionary)

	print "Outputing decoded data to file..."
	output_file_decoded = open('Data/output_test_decoded.tpc','w')

	output_file_decoded.write(decodedString)
	print "Finished!\n"

	if (decodedString == file_content):
		print "Decoding was successful!"


#------------------------------------------------------------------------------------------------------------------


rootDir = 'C:\Users\Crispino\Documents\GitHub\multimedia-information-systems\Project 2\Part 4\Data'#util.safeGetDirectory()
# allFiles = [f for f in listdir(rootDir) if isfile(join(rootDir,f))]
inputFileName =  'test.tpc'#util.getVideoFile(allFiles)

inputFilePath = rootDir + "/" + inputFileName

# print inputFilePath

inputFile = open(inputFilePath,'r')

# print inputFile
fileContent = inputFile.read()

#testing LZW
# LZW(fileContent)

#testing shannon-fano
shanonFano(fileContent)