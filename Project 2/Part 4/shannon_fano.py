from selection_sort import selectionSort
import sf_tree

def searchArray(value,array):
	for i in range(0,len(array)):
		if (value == array[i][0]):
			return i

	return -1

def stringFrequencyValues(string):
	"""computes 'string' and returns an 2-dimenstional array containing the frequencies
	   of each character of the string"""
	"""the returned array is formatted in the following way:
	   [ 
	     [*char1*,*number of itsappearances on the string],
	     [*char2*,*number of itsappearances on the string],
	    ...
	     [*charn*,*number of itsappearances on the string]  
	   ]"""
	frequency = []

	for i in string:
		position = searchArray(i,frequency)
		if (position != -1):
			frequency[position][1] += 1
		else:
			frequency.append([i,1])

	return frequency

def sumFrequency(frequency,i,j):
	#sum the frequency values of the "frequency" array from position "i" to "j"
	sum = 0

	if (i == j):
		sum += frequency[i][1]
	else:
		try:
			for x in range(i,j + 1):
				sum += frequency[x][1]	
		except IndexError:
			sum = -1

	return sum

def getPosition(frequency):
	#gets the position in which the array is going to be divided to be used by the Shannon-Fano algorithm

	smallerDifference = 1000000
	pos = 0

	for i in range(0,len(frequency)):
		difference = abs(sumFrequency(frequency,0,i) - sumFrequency(frequency,i + 1,len(frequency) - 1))
		if (difference < smallerDifference):
			smallerDifference = difference
			pos = i

	return pos

def getSymbols(frequency):
	"""gets the frequency array and returns an array 
	   with only the symbols of the to-be-encoded string"""
	return [i[0] for i in frequency]


def shannonFanoEncoder(frequency):
	"""gets the "frequency" array of symbol frequencies and the total frequency
	   of the symbols and encodes the given string"""

	position = getPosition(frequency)

	tree = sf_tree.sf_tree()
	tree.add(frequency,sf_tree.ROOT)
	

	length_freq = len(frequency)
	if (length_freq > 1):
		#print "inside if"
		if (position == 0):
			#in the case 'position' is 0, it has to be incremented so that 'leftFrequencies' doesn't become an empty list
			position += 1
		if (position + 1 == length_freq):
			# length_freq += 1
			pass

		if (length_freq == 2):
			leftFrequencies = [frequency[0]]
			rightFrequencies = [frequency[1]]
		else:
			leftFrequencies = [frequency[i] for i in range(0,position + 1)]
			rightFrequencies = [frequency[i] for i in range(position + 1,length_freq)]

		tree.lnode = (shannonFanoEncoder(leftFrequencies))
		tree.rnode = (shannonFanoEncoder(rightFrequencies))

	return tree

def setCodes(sftree,tmpcode):
	#sets the binary codes for each leaf of the tree
	if (sftree):
		if (len(sftree.value) == 1):
			sftree.value = [sftree.value[0][0],tmpcode]
		else:
			setCodes(sftree.lnode,tmpcode + '0')
			setCodes(sftree.rnode,tmpcode + '1')

def searchSymbol(symbol,sftree):
	#searchs for a symbol on the tree and returns its code
	if (sftree):
		if (sftree.value == symbol):
			return ""
		else:
			return "0" + searchSymbol(symbol,sftree.lnode)
			return "1" + searchSymbol(symbol,sftree.rnode)

def getCode(symbol,sftree,code):
	#searchs for 'symbol' on 'sftree' and generates a binary code according to its position on the tree and puts it into "code"
	#code must be a list, so it can be passed as reference by the recursive calls of the function
	if (sftree):
		if (sftree.value[0] == symbol):
			code.append(sftree.value[1])
		else:
			getCode(symbol,sftree.lnode,code)
			getCode(symbol,sftree.rnode,code)

def createDictionary(sftree,frequency):
	#takes an Shannon-Fano tree and creates an dictionary containing the codes for each symbol of the encoded string

	dictionary = {}

	for i in frequency:
		code = []
		symbol = i[0]
		getCode(symbol,sftree,code)
		dictionary[symbol] = code[0]

	return dictionary

def encodeString(string,dictionary):
	encodedString = ""

	for char in string:
		encodedString += dictionary[char]

	return encodedString

def searchCodeDictionary(code,dictionary):
	for symbol in dictionary:
		if (code == dictionary[symbol]):
			return symbol

	return 0

def decodeString(encodedString,dictionary):
	decodedString = ""
	s = ""

	for i in range(len(encodedString)):
		c = encodedString[i]
		s += c
		
		search = searchCodeDictionary(s,dictionary)
		if (search):
			#appends found symbol to 'decodedString'
			decodedString += search
			s = ""

	return decodedString

# string = "1231 782728 12732 19903 123276 193983 38748 09609 1272738 09230 -1 20 1- 2390 3-4"
string = '210$'

frequency = stringFrequencyValues(string)

selectionSort(frequency) #sorts the array based on the frequency...
frequency.reverse() #...then reverses it so that the biggest values come first
#-------------------------------------------------------------------------------
# print frequency

# print 'position'
# print getPosition(frequency)

print "Sorted symbol frequency values: "
print frequency
print
# ------------------------------------------------------------------------------
# print getPosition(frequency)

encodedTree = shannonFanoEncoder(frequency)

# encodedTree.print_tree_pre_order()

setCodes(encodedTree,"")
# print encodedTree.print_tree_pre_order()

# print
# encodedTree.print_tree_pre_order()

# print '\n'

dictionary = createDictionary(encodedTree,frequency)

# print 'dicitonary: '
# print dictionary
# print encodedTree.lnode.rnode.lnode.value

print "Original string: " + string

encodedString = encodeString(string,dictionary)

print "Encoded string: " + encodedString

decodedString = decodeString(encodedString,dictionary)

print "Decoded string: " + decodedString

if (decodedString == string):
	print "Decoding was successful!"