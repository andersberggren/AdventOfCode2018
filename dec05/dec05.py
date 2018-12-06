import re

#############
# Functions #
#############
def getPolymerFromFile(fileName):
	with open(fileName) as f:
		return f.read().strip()

def getReducedPolymer(polymer):
	i = 0
	while i+1 < len(polymer):
		unitA = polymer[i]
		unitB = polymer[i+1]
		if unitA.lower() == unitB.lower() and unitA != unitB:
			polymer = polymer[:i] + polymer[i+2:]
			if i > 0:
				i -= 1
		else:
			i += 1
	return polymer

########
# Main #
########
polymer = getPolymerFromFile("input05")

# Part 1
reducedPolymer = getReducedPolymer(polymer)
print("Size after reduction: {}".format(len(reducedPolymer)))

# Part 2
charToSize = {}
for char in "abcdefghijklmnopqrstuvwxyz":
	candidatePolymer = re.sub(char, "", reducedPolymer, flags=re.IGNORECASE)
	candidatePolymer = getReducedPolymer(candidatePolymer)
	charToSize[char] = len(candidatePolymer)
(char, size) = sorted(charToSize.items(), key=lambda item: item[1])[0]
print("Remove {char} to reduce the size to {size}".format(char=char.upper(), size=size))
