"""
	code used to sort the values frequency 
	values on Shannon-Fano algortithm
"""

def selectionSort(list):
	for i in range(0,len(list) - 1):
		smaller = i
		changed = False
		for j in range(i + 1,len(list)):
			if (list[j][1] < list[smaller][1]):
				smaller = j
				changed = True

		if (changed):
			swap(list,i,smaller)

def swap(list,pos1,pos2):
	aux = [list[pos1][0],list[pos1][1]]


	list[pos1][0] = list[pos2][0]
	list[pos1][1] = list[pos2][1]

	list[pos2][0] = aux[0]
	list[pos2][1] = aux[1]