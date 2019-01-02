class CircularList:
	""" A circular and doubly-linked list. """
	
	class Element:
		"""
		An element in the list, with references to the previous and next element in the list.
		"""
		def __init__(self, value):
			self.value = value
			self.prev = None
			self.next = None
	
	def __init__(self):
		self.cursor = None
		self.size = 0

	def insert(self, valueToInsert):
		"""
		Inserts "valueToInsert" before the cursor.
		After insert, the cursor points to the new element.
		"""
		newElement = CircularList.Element(valueToInsert)
		if self.size == 0:
			newElement.prev = newElement
			newElement.next = newElement
		else:
			prevElement = self.cursor.prev
			prevElement.next = newElement
			self.cursor.prev = newElement
			newElement.next = self.cursor
			newElement.prev = prevElement
		self.cursor = newElement
		self.size += 1

	def remove(self):
		"""
		Removes the element at the cursor, and returns the element.
		After remove, the cursor points to the element after the element that was removed.
		"""
		if self.size == 0:
			raise RuntimeError("Can't remove, size is 0")
		valueToReturn = self.cursor.value
		if self.size == 1:
			self.cursor = None
		else:
			prevElement = self.cursor.prev
			nextElement = self.cursor.next
			prevElement.next = nextElement
			nextElement.prev = prevElement
			self.cursor = nextElement
		self.size -= 1
		return valueToReturn

	def get(self):
		""" Returns the element at the cursor. """
		return self.cursor.value

	def moveCursor(self, numberOfSteps):
		""" Moves the cursor "numberOfSteps" steps (can be negative). """
		forward = numberOfSteps >= 0
		for i in range(abs(numberOfSteps)):  # @UnusedVariable
			if forward:
				self.cursor = self.cursor.next
			else:
				self.cursor = self.cursor.prev
