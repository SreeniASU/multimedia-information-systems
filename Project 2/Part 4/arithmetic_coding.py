#WHATS MISSING: 
# - Figure out how to get the probabilities for the symbols

terminator = "$" #value that indicates end of string

def floatBinToDecimal(bin):
	#converts a floating point binary to a decimal number
	#bin has to be a string
	
	n = 0

	for i in range(0,len(bin)): 
		n += (int(bin[i]))/float(2**(i + 1))


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
		range = high - low

		high = dictionary[char][1] * range + low
		low = dictionary[char][0] * range + low

		if (char == terminator):
			"""if char is the terminator, there is no need to execute
			the final part of the loop, so it is broken"""
			terminate = True
			break

		i += 1
		char = string[i]
		
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

string = 'CAEE$'
# string = '210$'
# dictionary = {'2':[0,0.2],'1':[0.2,0.6],'0':[0.6,0.9],terminator:[0.9,1]}
dictionary = {'A':[0,0.2],'B':[0.2,0.3],'C':[0.3,0.5],'D':[0.5,0.55],'E':[0.55,0.85],'F':[0.85,0.9],terminator:[0.9,1]}

#first, the final frequency interval is calculated for the given string
frequency_interval = frequencyInterval(string,dictionary)

code = arithmetic_encode(frequency_interval)

decoded_string = arithmetic_decode(code,dictionary)


print 'Original string: ' + string
print 'Encoded string: ' + code
print "Decoded string: " + decoded_string

if (decoded_string == string):
	print "Decoding was successful!"