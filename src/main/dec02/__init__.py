from aoclib.filereader import getFileAsSingleString

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
	return any([x == numberOfTimes for x in charCounter.values()])

def findMatchingBoxIDs(boxIDs):
	return next((a,b) for a in boxIDs for b in boxIDs if isIdenticalExceptForOneCharacter(a, b))

def isIdenticalExceptForOneCharacter(boxID1, boxID2):
	if len(boxID1) != len(boxID2):
		raise ValueError("boxID1 and boxID2 have different lengths")
	return len([1 for i in range(0, len(boxID1)) if boxID1[i] != boxID2[i]]) == 1

def getCorrectBoxID(boxID1, boxID2):
	diffIndex = next(i for i in range(0, len(boxID1)) if boxID1[i] != boxID2[i])
	return boxID1[0:diffIndex] + boxID1[diffIndex+1:]

########
# Main #
########
boxIDs = getFileAsSingleString("input02.txt").split()

# Part 1
twoTimes   = len([boxID for boxID in boxIDs if hasCharacterOccurringExactlyThisManyTimes(boxID, 2)])
threeTimes = len([boxID for boxID in boxIDs if hasCharacterOccurringExactlyThisManyTimes(boxID, 3)])
print("Checksum: {}".format(twoTimes * threeTimes))

# Part 2
(boxID1, boxID2) = findMatchingBoxIDs(boxIDs)
correctBoxID = getCorrectBoxID(boxID1, boxID2)
print("Correct box ID: {}".format(correctBoxID))
