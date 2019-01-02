from aoclib.filereader import getFileAsSingleString

#############
# Functions #
#############
def findFirstRepeatedFrequency(initialFrequency, frequencyChangeList):
	currentFrequency = initialFrequency
	previousFrequencies = {currentFrequency}
	while True:
		for delta in frequencyChangeList:
			currentFrequency += delta
			if currentFrequency in previousFrequencies:
				return currentFrequency
			else:
				previousFrequencies.add(currentFrequency)

########
# Main #
########
frequencyChangeList = [int(x) for x in getFileAsSingleString("input01.txt").split()]

# Part 1: What is the final frequency after applying all the changes in the list (once)?
print("Final frequency: {}".format(sum(frequencyChangeList)))

# Part 2: Which is the first frequency that is reached twice?
firstRepeatedFrequency = findFirstRepeatedFrequency(0, frequencyChangeList)
print("First repeated frequency: {}".format(firstRepeatedFrequency))
