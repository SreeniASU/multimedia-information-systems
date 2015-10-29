
#ISSUE: codes for each character have to be binaries, not decimals

def createDictionary(string,dictionary):
	#creates the dictionary based on the string passed as argument
	for c in string:
		if (searchInDictionary(c,dictionary) == -1):
			dictionary[c] = len(dictionary) + 1

def searchInDictionary(string,dictionary):
	#searchs in dictionary if the string "string" is located there
	try:
		return dictionary[string]
	except KeyError:
		return -1

def lzwEncoder(string,dicitonary):
	s = string[0]
	output_code = [] #code to be outputed at the end(treated as an array)

	for i in range(0,len(string)):
		if (i == 0): continue
		c = string[i]

		search = searchInDictionary(s + c,dictionary)
		if (search != -1):
			s += c
		else:
			output = dictionary[s]
			dictionary[s + c] = len(dictionary) + 1
			s = c

			output_code.append(str(output))

	output_code.append(str(dictionary[c])) #adds to the code the symbol read at the end of the file

	return output_code

def lzwDecoder(code,dictionary):
	decoded_string = ""

	for c in code:
		for i in dictionary:
			if (str(dictionary[i]) == c):
				decoded_string += i

	return decoded_string

string = "Use the join method of the empty string to join all of the strings together with the empty string in between, like so:	"

dictionary = {}

createDictionary(string,dictionary)

print ("Original string: " + string)

encoded_string = lzwEncoder(string,dictionary)

print("Encoded string: " + ''.join(encoded_string))

decoded_string = lzwDecoder(encoded_string,dictionary)

print("Decoded string: " + decoded_string)

if (string == decoded_string):
	print "Decoding was successful!"


# print dictionary
