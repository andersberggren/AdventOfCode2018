import re

###########
# Classes #
###########
class Generation:
	# index  The index of this generation (0, 1, 2, ...)
	# plants           A set of integers, representing the indices of pots with plants.
	# spreadPatterns   A set of strings, representing the patterns that
	#                  lead to a plant next generation.
	def __init__(self, index, plants, spreadPatterns):
		self.index = index
		self.plants = plants
		self.spreadPatterns = spreadPatterns

	# Creates and returns a new Generation-object, representing the next generation of plants.
	def createNextGeneration(self):
		minPlantIndex = min(self.plants)
		maxPlantIndex = max(self.plants)
		indexRange = range(minPlantIndex-2, maxPlantIndex+3)
		newPlants = set([i for i in indexRange if self.getPatternForPot(i) in self.spreadPatterns])
		return Generation(self.index+1, newPlants, self.spreadPatterns)

	# Returns a string with the pattern around this pot.
	def getPatternForPot(self, potIndex):
		pattern = ""
		for i in range(potIndex-2, potIndex+3):
			if i in self.plants:
				pattern += "#"
			else:
				pattern += "."
		return pattern

	# Returns the sum of the indices of all pots with plants.
	def getSum(self):
		return sum(self.plants)

	# Returns the plants as a string, where "#" is a pot with plant, and "." is a pot without plant.
	# The first character of the string is the leftmost pot that contains a plant,
	# regardless of index.
	def getPlantsAsString(self):
		minIndex = min(self.plants)
		maxIndex = max(self.plants)
		plantsAsString = ""
		for i in range(minIndex, maxIndex+1):
			if i in self.plants:
				plantsAsString += "#"
			else:
				plantsAsString += "."
		return plantsAsString

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
			matchInitialPlants = re.match("initial state: ([#.]+)$", line)
			matchSpreadPattern = re.match("([#.]{5}) => #", line)
			if matchInitialPlants:
				initialPlants = getPlantsFromString(matchInitialPlants.group(1))
			elif matchSpreadPattern:
				spreadPatterns.add(matchSpreadPattern.group(1))
	return (initialPlants, spreadPatterns)

# Reads plantsAsString, and returns a set of integers, containing the
# indices of pots with plants.
def getPlantsFromString(plantsAsString):
	initialPlants = set()
	for i in range(len(plantsAsString)):
		if plantsAsString[i] == "#":
			initialPlants.add(i)
	return initialPlants

# Returns (plantSum, generations), where:
# - plantSum is the plant index sum of the generation with numberOfGenerations.
# - generations is a list of all created Generation-objects.
def getSumOfGeneration(generationZero, numberOfGenerations):
	generations = [generationZero]
	plantPatternToGenerationIndex = {generationZero.getPlantsAsString(): generationZero.index}
	
	# Create new generations, until we either:
	# - reach numberOfGenerations.
	# - find a repeated plant pattern, and can calculate the sum of the final generation,
	#   without having to calculate all the generations in between.
	while generations[-1].index < numberOfGenerations:
		newGeneration = generations[-1].createNextGeneration()
		generations.append(newGeneration)
		plantPattern = newGeneration.getPlantsAsString()
		if plantPattern in plantPatternToGenerationIndex:
			# We have found a repeated pattern
			prevGeneration = generations[plantPatternToGenerationIndex[plantPattern]]
			numberOfGenerationsLeft = numberOfGenerations - newGeneration.index
			loopSize = newGeneration.index - prevGeneration.index
			(numberOfLoops, remainder) = divmod(numberOfGenerationsLeft, loopSize)
			plantSumDeltaPerLoop = newGeneration.getSum() - prevGeneration.getSum()
			plantSum = newGeneration.getSum()
			plantSum += numberOfLoops * plantSumDeltaPerLoop
			plantSum += generations[prevGeneration.index+remainder].getSum() \
					- prevGeneration.getSum()
			return (plantSum, generations)
		else:
			plantPatternToGenerationIndex[plantPattern] = newGeneration.index
	return (generations[-1].getSum(), generations)

# Prints text to visually represent the plant generations in "generations".
def printGenerations(generations):
	minIndex = min([min(g.plants) for g in generations])
	maxIndex = max([max(g.plants) for g in generations])
	generationIndexLen = len(str(max([g.index for g in generations])))
	print("Plant generations 0-{gen}, with pot index from {min} to {max}:".format(
			gen=generations[-1].index, min=minIndex, max=maxIndex))
	for generation in generations:
		plantsAsString = "{gen: >{len}} ".format(gen=generation.index, len=generationIndexLen)
		for i in range(minIndex, maxIndex+1):
			if i in generation.plants:
				plantsAsString += "#"
			else:
				plantsAsString += "."
		print(plantsAsString)

########
# Main #
########
(plants, spreadPatterns) = getInitialPlantsAndSpreadPatternsFromFile("input12")
generationZero = Generation(0, plants, spreadPatterns)

for i in [20, 50000000000]:
	(plantSum, generations) = getSumOfGeneration(generationZero, i)
	printGenerations(generations)
	print("Generation {gen} plant sum: {sum}".format(gen=i, sum=plantSum))
