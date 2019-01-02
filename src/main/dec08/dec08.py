#############
# Functions #
#############
def getIntegerListFromFile(fileName):
	with open(fileName) as f:
		return [int(word) for word in f.read().split()]

# Reads from integerList, and returns the metadata sum of the next node (including its children).
# The integers that are read will be removed from the list.
def getValueOfNodePart1(integerList):
	numberOfChildren = integerList.pop(0)
	numberOfMetadataEntries = integerList.pop(0)
	metadataSum = 0
	for i in range(numberOfChildren):
		metadataSum += getValueOfNodePart1(integerList)
	for i in range(numberOfMetadataEntries):
		metadataSum += integerList.pop(0)
	return metadataSum

# Reads from integerList, and returns the value of the next node,
# calculated according to the rules of part 2.
# The integers that are read will be removed from the list.
def getValueOfNodePart2(integerList):
	numberOfChildren = integerList.pop(0)
	numberOfMetadataEntries = integerList.pop(0)
	# Dict, from child node index (starting at 1), to value of corresponding node
	childNodeToValue = {}
	nodeValue = 0
	for i in range(numberOfChildren):
		childNodeToValue[i+1] = getValueOfNodePart2(integerList)
	for i in range(numberOfMetadataEntries):
		metadata = integerList.pop(0)
		if numberOfChildren == 0:
			# Node has no children. Add metadata value.
			nodeValue += metadata
		else:
			try:
				# Node has children. Add value from child node with index "metadata".
				nodeValue += childNodeToValue[metadata]
			except KeyError:
				# Invalid metadata index. Ignore.
				pass
	return nodeValue

########
# Main #
########
# Part 1
integerList = getIntegerListFromFile("input08.txt")
print("Metadata sum of all nodes: {}".format(getValueOfNodePart1(integerList)))

# Part 2
integerList = getIntegerListFromFile("input08.txt")
print("Value of root node (part 2): {}".format(getValueOfNodePart2(integerList)))
