"""
	Auxiliary tree data structure used on the Shannon-Fano algorithm
	
"""

LEFT = 0
RIGHT = 1
ROOT = 2

class sf_tree:
	def __init__(self):
		self.rnode = None
		self.lnode = None
		self.value = None

	def add(self,value,type):
		if (self.value == None):
			self.value = value
		elif (type == RIGHT):
			if (self.rnode == None):
				self.rnode = sf_tree()
			self.rnode.value = value
		elif (type == LEFT):
			if (self.lnode == None):
				self.lnode = sf_tree()
			self.lnode.value = value
		elif (type == ROOT):
			self.value = value
		else:
			print("Wrong argument at 'add' function!")


	def print_tree_in_order(self):
		if (self):
			if (self.lnode): self.lnode.print_tree_in_order()
			print self.value
			if (self.rnode): self.rnode.print_tree_in_order()

	def print_tree_pre_order(self):
		if (self):
			print self.value
			if (self.lnode): self.lnode.print_tree_pre_order()
			if (self.rnode): self.rnode.print_tree_pre_order()