from decimal import *
#library used to prevent rounding in large float numbers

#WHATS MISSING: 
# - Figure out how to get the probabilities for the symbols

getcontext().prec = 500 #precision of the floating point numbers

terminator = "$" #value that indicates end of string

def updateString(string):
	#adds the terminator character if not present
	length = len(string)

	if (string[length - 1] != terminator):
		string += terminator
		length += 1

	return string

def createDictionary(string):
	dictionary = {}

	len_str = len(string)

	for char in string:
		#counts how many times each symbol appears on the
		#string and adds this information to 'dictionary'
		try:
			dictionary[char] += 1
		except KeyError:
			dictionary[char] = 1

	# len_dic = len(dictionary)
	# print len_dic

	low = 0
	for char in dictionary:
		#modifies the format of the dictionary such that now
		#its value for each char is an array containing the 
		#interval '[low,high)' for its probability
		symbol_count = dictionary[char]
		probability = Decimal(str(symbol_count/Decimal(str(len_str))))
		dictionary[char] = [low,low + probability]
		# low += Decimal(str(symbol_count/float(len_str)))
		low += Decimal(symbol_count/Decimal(len_str))

	return dictionary


def floatBinToDecimal(bin):
	#converts a floating point binary to a decimal number
	#bin has to be a string
	
	n = 0

	for i in range(0,len(bin)): 
		# n += Decimal( str( int(bin[i])/Decimal( float(2**(i + 1)) ) ) )
		n += Decimal( int(bin[i])/Decimal(2**(i + 1)) )  


	return n

def frequencyInterval(string,dictionary):
	"""computes the given "string" and according to the "dictionary" values, 
	it returns its corresponding [low,high) final interval"""
	low = 0
	high = 1
	terminate = False #this variable becomes true when the terminator char is found

	i = 0
	char = string[i]
	while (not terminate):
		# print 'char: ' + char
		rng = high - low
		# print "char,low,high: " + char + ',' + str(dictionary[char][0]) + ',' + str(dictionary[char][1])
		# print "high,low,range: " + str(high) + ',' + str(low) + ',' + str(rng)

		# if (char == 'o'):
			# if (low == 0.255645751953125): 
				# print "EQUALS!!"

		"""if (low == 0.25537109375):
			print dictionary[char][0]
			print rng
			print low
			print 'HIGH!!!'
			print dictionary[char][0] * rng + low
			print "range: "
			print rng
			print"""

		high = dictionary[char][1] * rng + low

		low = dictionary[char][0] * rng + low

		if (char == terminator):
			"""if char is the terminator, there is no need to execute
			the final part of the loop, so it is broken"""
			terminate = True
			break

		i += 1
		char = string[i]
		
	"""if (low == high):
		lst = [int(str(low)[i]) for i in range(2,len(str(low)))]
		lst.pop()
		nstr = "0."
		for i in lst: nstr += str(i)
		low = float(nstr)"""

	# if (low == high):
		# print 'EQUALS!!!'

	return low,high

def arithmetic_encode(frequency_interval):
	#encode the given string based on the interval "[low,high)"
	low = frequency_interval[0]
	high = frequency_interval[1]
	code = ['0']
	k = 1

	while(floatBinToDecimal(''.join(code)) < low):
		if (k == 1):
			code[k - 1] = '1'
		else:
			code.append('1')

		if (floatBinToDecimal(''.join(code)) > high):
			code[k - 1] = '0'

		k += 1

	return ''.join(code) 

def find_symbol(value,dictionary):
	for symbol in dictionary:
		if (dictionary[symbol][0] <= value and value < dictionary[symbol][1]):
			return symbol

def arithmetic_decode(bin_code,dictionary):
	"""with the decoded code "bin_code" and dictionary "dictionary", it decodes the code, 
	   returning the decoded string"""

	decoded_string = ""
	symbol = ""
	decimal_value = floatBinToDecimal(bin_code)

	while (symbol != terminator):
		symbol = find_symbol(decimal_value,dictionary)
		decoded_string += symbol

		low = dictionary[symbol][0]
		high = dictionary[symbol][1]
		rng = high - low

		decimal_value = (decimal_value - low)/rng

	return decoded_string

string = 'CAEE'
string = updateString(string)
dictionary = createDictionary(string)

# print dictionary

# string = 'CAEE$'
# string = '210$'
# dictionary = {'2':[0,0.2],'1':[0.2,0.6],'0':[0.6,0.9],terminator:[0.9,1]}
# dictionary = {'A':[0,0.2],'B':[0.2,0.3],'C':[0.3,0.5],'D':[0.5,0.55],'E':[0.55,0.85],'F':[0.85,0.9],terminator:[0.9,1]}


#first, the final frequency interval is calculated for the given string
frequency_interval = frequencyInterval(string,dictionary)

print "Frequency interval: " + str(frequency_interval)

code = arithmetic_encode(frequency_interval)

decoded_string = arithmetic_decode(code,dictionary)


print 'Original string: ' + string
print 'Encoded string: ' + code
print "Decoded string: " + decoded_string

if (decoded_string == string):
	print "Decoding was successful!"