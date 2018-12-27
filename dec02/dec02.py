#############
# Functions #
#############
def hasCharacterOccurringExactlyThisManyTimes(boxID, numberOfTimes):
	charCounter = {}
	for char in boxID:
		if char in charCounter:
			charCounter[char] += 1
		else:
			charCounter[char] = 1
	for (char, occurrences) in charCounter.items():
		if occurrences == numberOfTimes:
			return True
	return False

def findMatchingBoxIDs(boxIDs):
	for boxID1 in boxIDs:
		for boxID2 in boxIDs:
			if isIdenticalExceptForOneCharacter(boxID1, boxID2):
				return (boxID1, boxID2)
	raise RuntimeError("Could not find the two matching box IDs")

def isIdenticalExceptForOneCharacter(boxID1, boxID2):
	if len(boxID1) != len(boxID2):
		raise ValueError("boxID1 and boxID2 have different lengths")

	numberOfDifferingCharacters = 0
	for i in range(0, len(boxID1)):
		if boxID1[i] != boxID2[i]:
			numberOfDifferingCharacters += 1
			if numberOfDifferingCharacters > 1:
				return False
	return numberOfDifferingCharacters == 1

def getCorrectBoxID(boxID1, boxID2):
	for i in range(0, len(boxID1)):
		if boxID1[i] != boxID2[i]:
			return boxID1[0:i] + boxID1[i+1:]

########
# Main #
########
with open("input02.txt") as f:
	boxIDs = f.read().split()

# Part 1
twoTimes = 0
threeTimes = 0
for boxID in boxIDs:
	if hasCharacterOccurringExactlyThisManyTimes(boxID, 2):
		twoTimes += 1
	if hasCharacterOccurringExactlyThisManyTimes(boxID, 3):
		threeTimes += 1
print("Two times: {}".format(twoTimes))
print("Three times: {}".format(threeTimes))
print("Checksum: {}".format(twoTimes * threeTimes))

# Part 2
(boxID1, boxID2) = findMatchingBoxIDs(boxIDs)
print("Box ID 1: {}".format(boxID1))
print("Box ID 2: {}".format(boxID2))
correctBoxID = getCorrectBoxID(boxID1, boxID2)
print("Correct box ID: {}".format(correctBoxID))
