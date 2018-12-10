#############
# Functions #
#############
def getIntegerListFromFile(fileName):
	with open(fileName) as f:
		return [int(word) for word in f.read().split()]

# Returns the metadata sum of the node (including its children).
def getValueOfNode(integerList):
	numberOfChildren = integerList.pop(0)
	numberOfMetadataEntries = integerList.pop(0)
	metadataSum = 0
	for i in range(numberOfChildren):
		metadataSum += getValueOfNode(integerList)
	for i in range(numberOfMetadataEntries):
		metadataSum += integerList.pop(0)
	return metadataSum

########
# Main #
########
integerList = getIntegerListFromFile("input08")
metadataSum = getValueOfNode(integerList)
print("Metadata sum: {}".format(metadataSum))
