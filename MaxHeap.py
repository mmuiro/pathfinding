# Binary MaxHeap Class. For use with A-Star. Made with more "convential" OOP in mind, and meant to be thorough.

class MaxHeap():

	def __init__(self, comparator=lambda x,y: x-y, items=[]):
		self.comparator = comparator # A function used to compare items.
		self.size = 0
		self.items = []
		for item in items:
			slef.insert(item)

	# Inserts an item into the Heap.
	def insert(self, item):
		self.items.append(item)
		self.size += 1
		self.adjustUp(self.size - 1)

	# Rebalances the heap, going up from index i.
	def adjustUp(self, i):
		if self.getParent(i) != None and self.comparator(self.get(i), self.getParent(i)) > 0:
			parentIndex = self.getParentIndex(i)
			self.swap(i, parentIndex)
			self.adjustUp(parentIndex)

	# Returns the item at index i. Assumes valid index.
	def get(self, i):
		return self.items[i]

	# Removes the "largest" item in the heap.
	def pop(self):
		if self.is_empty():
			return None
		return self.remove(0)

	# Removes the item at index i. Assumes valid index.
	def remove(self, i):
		self.swap(i, self.size-1)
		retItem = self.items.pop()
		self.size -= 1
		self.adjustDown(i)
		return retItem

	# Rebalances the heap, going down from index i.
	def adjustDown(self, i=0):
		if self.getRightChild(i) != None and self.comparator(self.get(i), self.getRightChild(i)) < 0:
			rightChildIndex = self.getRightChildIndex(i)
			self.swap(i, rightChildIndex)
			self.adjustDown(rightChildIndex)
		if self.getLeftChild(i) != None and self.comparator(self.get(i), self.getLeftChild(i)) < 0:
			leftChildIndex = self.getLeftChildIndex(i)
			self.swap(i, leftChildIndex)
			self.adjustDown(leftChildIndex)


	# Swaps the items at the two indeces. Assumes indices are valid.
	def swap(self, i, j):
		temp = self.items[i]
		self.items[i] = self.items[j]
		self.items[j] = temp

	# Returns if the heap is empty.
	def is_empty(self):
		return self.size == 0

	# Returns the left child of item at index i.
	def getLeftChild(self, i):
		leftChildIndex = self.getLeftChildIndex(i)
		if i < 0 or i >= self.size or leftChildIndex >= self.size:
			return None
		return self.items[leftChildIndex]

	# Returns the index of the left child of item at index i.
	def getLeftChildIndex(self, i):
		return 2 * i + 1

	# Returns the right child of item at index i.
	def getRightChild(self, i):
		rightChildIndex = self.getRightChildIndex(i)
		if i < 0 or i >= self.size or rightChildIndex >= self.size:
			return None
		return self.items[rightChildIndex]

	# Returns the index of the right child of item at index i.
	def getRightChildIndex(self, i):
		return 2 * (i + 1)

	# Returns the parent of the item at index i.
	def getParent(self, i):
		parentIndex = self.getParentIndex(i)
		if i < 0 or i >= self.size or parentIndex < 0:
			return None
		return self.items[parentIndex]

	# Returns the parent index of the item at index i.
	def getParentIndex(self, i):
		return (i - 1) // 2

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		if self.is_empty():
			return ""
		retstr = ""
		pow2sum, nextexp = 0, 1
		for i in range(len(self.items)):
			retstr += str(self.items[i]) + " "
			if i == pow2sum:
				retstr += "\n"
				pow2sum += pow(2, nextexp)
				nextexp += 1
		return retstr[:-1]


