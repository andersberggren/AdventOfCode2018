class SortedList:
	def __init__(self):
		self.head = None
	
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
	
	def pop(self):
		if self.isEmpty():
			raise RuntimeError("Called pop() on empty list")
		itemToReturn = self.head.value
		self.head = self.head.next
		return itemToReturn
	
	def getSize(self):
		itemIterator = self.head
		size = 0
		while itemIterator is not None:
			size += 1
			itemIterator = itemIterator.next
		return size
	
	def isEmpty(self):
		return self.head is None

	class ListItem:
		def __init__(self, value, nextItem=None):
			self.value = value
			self.next = nextItem
