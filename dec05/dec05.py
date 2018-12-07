import re
import string

#############
# Functions #
#############
def getPolymerFromFile(fileName):
	with open(fileName) as f:
		return f.read().strip()

# Reduce the polymer by removing adjacent units of the same type and opposite polarity,
# i.e. adjacent characters of the same letter where one is upper case and the other is lower case.
def getReducedPolymer(polymer):
	i = 0
	while i+1 < len(polymer):
		unitA = polymer[i]
		unitB = polymer[i+1]
		sameType = unitA.lower() == unitB.lower()
		oppositePolarity = unitA.islower() != unitB.islower()
		if sameType and oppositePolarity:
			polymer = polymer[:i] + polymer[i+2:]
			if i > 0:
				i -= 1
		else:
			i += 1
	return polymer

# Answers the question "Which unit should be removed to then be able to reduce the polymer to the
# smallest size?".
# Returns a tuple (unit, size), where "unit" is the unit to remove, and "size" is the size of the
# polymer after removing all occurrences of "unit" and then reducing.
def findBestUnitToRemove(polymer):
	charToSize = {}
	# string.ascii_uppercase = "ABC...Z"
	for char in string.ascii_uppercase:
		candidatePolymer = re.sub(char, "", polymer, flags=re.IGNORECASE)
		candidatePolymer = getReducedPolymer(candidatePolymer)
		charToSize[char] = len(candidatePolymer)
	return sorted(charToSize.items(), key=lambda item: item[1])[0]

########
# Main #
########
polymer = getPolymerFromFile("input05")

# Part 1
polymer = getReducedPolymer(polymer)
print("Size after reduction: {}".format(len(polymer)))

# Part 2
(char, size) = findBestUnitToRemove(polymer)
print("Remove unit {char} to reduce the size to {size}".format(char=char, size=size))
