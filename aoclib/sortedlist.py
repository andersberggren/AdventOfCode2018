class SortedList:
	def __init__(self):
		self.head = None
		self.size = 0
	
	def insert(self, valueToInsert):
		itemIterator = self.head
		prevItem = None
		while itemIterator is not None and itemIterator.value < valueToInsert:
			prevItem = itemIterator
			itemIterator = itemIterator.next
		newItem = SortedList.ListItem(valueToInsert, itemIterator)
		if prevItem is None:
			self.head = newItem
		else:
			prevItem.next = newItem
		self.size += 1
	
	def pop(self):
		if self.isEmpty():
			raise RuntimeError("Called pop() on empty list")
		itemToReturn = self.head.value
		self.head = self.head.next
		self.size -= 1
		return itemToReturn
	
	def getSize(self):
		return self.size
	
	def isEmpty(self):
		return self.size == 0

	class ListItem:
		def __init__(self, value, nextItem=None):
			self.value = value
			self.next = nextItem
