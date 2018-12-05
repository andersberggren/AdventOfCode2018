#############
# Functions #
#############
def findFirstRepeatedFrequency(initialFrequency, frequencyChangeList):
	currentFrequency = initialFrequency
	previousFrequencies = set([currentFrequency])
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
with open("input01") as f:
	fileContents = f.read()
	frequencyChangeList = [int(frequencyChange) for frequencyChange in fileContents.split()]

# Part 1: What is the final frequency after applying all the changes in the list (once)?
currentFrequency = 0
for freqChange in frequencyChangeList:
	currentFrequency += freqChange
print("Final frequency: {}".format(currentFrequency))

# Part 2: Which is the first frequency that is reached twice?
firstRepeatedFrequency = findFirstRepeatedFrequency(0, frequencyChangeList)
print("First repeated frequency: {}".format(firstRepeatedFrequency))
