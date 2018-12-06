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
			#print("Unit {} and {} can be reduced!".format(unitA, unitB))
			polymer = polymer[:i] + polymer[i+2:]
			print("Polymer size: {size}, i: {i}, removed {unit}".format(size=len(polymer), i=i, unit=unitA.upper()))
			if i > 0:
				i -= 1
		else:
			i += 1
	return polymer

########
# Main #
########
polymer = getPolymerFromFile("input05")
#polymer = "dabAcCaCBAcCcaDA"
print("Initial size: {}".format(len(polymer)))
polymer = getReducedPolymer(polymer)
print("Size after reduction: {}".format(len(polymer)))
print("Answer to part 1: {}".format(polymer))
