import re

#############
# Functions #
#############
# Returns (initialState, spreadPatterns), where:
# - initialState is a set of integers, representing the indices of plants.
# - spreadPatterns is a set of strings, representing the patterns that lead to
#   a plant next generation.
def getInitialStateAndSpreadPatternsFromFile(fileName):
	initialState = None
	spreadPatterns = set()
	with open(fileName) as f:
		for line in f.readlines():
			matchInitialState =  re.match("initial state: ([#.]+)$", line)
			matchSpreadPattern = re.match("([#.]{5}) => #", line)
			if matchInitialState:
				initialState = getInitialState(matchInitialState.group(1))
			elif matchSpreadPattern:
				spreadPatterns.add(matchSpreadPattern.group(1))
	return (initialState, spreadPatterns)

def getInitialState(initialStateAsString):
	initialState = set()
	for i in range(len(initialStateAsString)):
		if initialStateAsString[i] == "#":
			initialState.add(i)
	return initialState

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
(plants, spreadPatterns) = getInitialStateAndSpreadPatternsFromFile("input12")

#print("Plants at {}".format(sorted(plants)))
#print("Spread patterns:")
#[print(pattern) for pattern in sorted(spreadPatterns)]

for i in range(20):
	plants = getNextGenerationOfPlants(plants, spreadPatterns)
print(sum(plants))