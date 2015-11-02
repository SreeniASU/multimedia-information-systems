from cStringIO import StringIO
#ISSUE: codes for each character have to be binaries, not decimals

def createDictionary(string):
	#creates the dictionary based on the string passed as argument
	dictionary = {}

	for c in string:
		if (searchInDictionary(c,dictionary) == -1):
			dictionary[c] = len(dictionary) + 1

	return dictionary

def searchInDictionary(string,dictionary):
	#searchs in dictionary if the string "string" is located there
	try:
		return dictionary[string]
	except KeyError:
		return -1

def updateDictionary(dictionary):
	#convert the codes on the dictionary to binary numbers
	bin_length = len(bin(len(dictionary))[2:])

	for symbol in dictionary:
		code = dictionary[symbol]
		binary = bin(int(code))[2:]
		while(len(binary) < bin_length):
			binary = '0' + binary

		dictionary[symbol] = binary


	return dictionary

def updateEncodedString(encoded_string,dictionary):
	#convert the codes on the encoded string list to binary numbers
	bin_length = len(bin(len(dictionary))[2:])

	for i in range(0,len(encoded_string)):
		binary = bin(int(encoded_string[i]))[2:]
		while(len(binary) < bin_length):
			binary = '0' + binary
		encoded_string[i] = binary

	# print dictionary

	return encoded_string

def lzwEncoder(string,bitLength):

	dictionary = dict((chr(i), chr(i)) for i in xrange(bitLength))

	output = ""
	encoded = []
	for char in string:
		pattern = output + char

		if pattern in dictionary:
			output = pattern
		else:
			encoded.append(dictionary[output])
			dictionary[pattern] = bitLength
			bitLength += 1
			output = char #reset out pattern

	if (output):
		encoded.append(dictionary[output])

	return encoded

def lzwDecoder(encoded,bitLength):
	dictionary = dict((chr(i), chr(i)) for i in xrange(bitLength))

	decoded = StringIO()

	output = encoded.pop(0)
	decoded.write(output)

	for char in encoded:
		if (char in dictionary):
			entry = dictionary[char]
		elif (char == bitLength):
			entry = output + output[0]

		decoded.write(entry)

		dictionary[bitLength] = output + entry[0]
		bitLength += 1

		output = entry

	return decoded.getvalue()
