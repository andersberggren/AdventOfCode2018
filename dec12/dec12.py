import re

#############
# Functions #
#############
# Returns (initialPlants, spreadPatterns), where:
# - initialPlants is a set of integers, representing the indices of pots with plants.
# - spreadPatterns is a set of strings, representing the patterns that lead to
#   a plant next generation.
def getInitialPlantsAndSpreadPatternsFromFile(fileName):
	initialPlants = None
	spreadPatterns = set()
	with open(fileName) as f:
		for line in f.readlines():
			matchInitialPlants =  re.match("initial state: ([#.]+)$", line)
			matchSpreadPattern = re.match("([#.]{5}) => #", line)
			if matchInitialPlants:
				initialPlants = getInitialPlants(matchInitialPlants.group(1))
			elif matchSpreadPattern:
				spreadPatterns.add(matchSpreadPattern.group(1))
	return (initialPlants, spreadPatterns)

def getInitialPlants(initialPlantsAsString):
	initialPlants = set()
	for i in range(len(initialPlantsAsString)):
		if initialPlantsAsString[i] == "#":
			initialPlants.add(i)
	return initialPlants

def getNextGenerationOfPlants(plantsCurrentGeneration, spreadPatterns):
	plantsNextGeneration = set()
	minPlantIndex = min(plantsCurrentGeneration)
	maxPlantIndex = max(plantsCurrentGeneration)
	for plantIndex in range(minPlantIndex-2, maxPlantIndex+3):
		pattern = getPatternForPlant(plantsCurrentGeneration, plantIndex)
		if pattern in spreadPatterns:
			plantsNextGeneration.add(plantIndex)
	return plantsNextGeneration

# Returns a string (size: 5) with the pattern around this pot.
def getPatternForPlant(plants, plantIndex):
	pattern = ""
	for i in range(plantIndex-2, plantIndex+3):
		if i in plants:
			pattern += "#"
		else:
			pattern += "."
	return pattern

########
# Main #
########
(plants, spreadPatterns) = getInitialPlantsAndSpreadPatternsFromFile("input12")

#print("Plants at {}".format(sorted(plants)))
#print("Spread patterns:")
#[print(pattern) for pattern in sorted(spreadPatterns)]
generationToPlants = {0: plants}
numberOfGenerations = 100
for i in range(1, numberOfGenerations+1):
	plants = getNextGenerationOfPlants(plants, spreadPatterns)
	generationToPlants[i] = plants
	print("After {gen} generations, the sum of indices of pots with plants is {sum}".format(
			gen=i, sum=sum(plants)))

allPotsThatHasContainedAPlant = set()
for plants in generationToPlants.values():
	[allPotsThatHasContainedAPlant.add(x) for x in plants]
minIndex = min(allPotsThatHasContainedAPlant)
maxIndex = max(allPotsThatHasContainedAPlant)

print("Min index: {}".format(minIndex))
for generationIndex in range(0, max(generationToPlants.keys())+1):
	plants = generationToPlants[generationIndex]
	s = ""
	for i in range(minIndex, maxIndex+1):
		if i in plants:
			s += "#"
		else:
			s += "."
	print(s)
