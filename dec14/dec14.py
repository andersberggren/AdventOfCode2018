#############
# Functions #
#############
# Arguments:
#   recipeScores     Recipe scores (list of integers).
#   elves            Index in recipeScores where an elf is at (a list of integers).
#   numberOfRecipes  The number of recipe scores to generate, before the answer.
#   answerSize       The number of recipe scores, after numberOfRecipes, that will make up the answer.
#
# Returns a string with the answerSize digits that follows after generating numberOfRecipes recipes.
def part1(recipeScores, elves, numberOfRecipes, answerSize):
	recipeScores = recipeScores.copy()
	elves = elves.copy()
	while len(recipeScores) < numberOfRecipes+answerSize:
		appendScoresForNewRecipesAndMoveElves(recipeScores, elves)
	return "".join([str(d) for d in recipeScores[numberOfRecipes:numberOfRecipes+answerSize]])

# Arguments:
#   recipeScores   A list of integers, representing scores for recipes
#   elves          A list of integers, representing the index in recipeScores where an elf is at.
#   digitSequence  A list of integers. This is the sequence of digits we look for in recipeScores.
#
# Returns the number of recipe scores that need to be generated,
# before recipe scores occur according to digitSequence.
def part2(recipeScores, elves, digitSequence):
	while True:
		numberOfNewScores = appendScoresForNewRecipesAndMoveElves(recipeScores, elves)
		for i in range(numberOfNewScores):
			offset = len(recipeScores) - len(digitSequence) - i
			if matchSubList(recipeScores, digitSequence, offset):
				return offset
			if len(recipeScores) % 100000 == 0:
				print("{: >11,} recipes created".format(len(recipeScores)), flush=True)

# Appends new recipe scores (one or two) at the end of recipeScores,
# and moves the elves to new recipes.
# Returns the number of recipe scores added.
def appendScoresForNewRecipesAndMoveElves(recipeScores, elves):
	scoreSumAsString = str(sum([recipeScores[elf] for elf in elves]))
	for digitAsString in scoreSumAsString:
		recipeScores.append(int(digitAsString))
	for i in range(len(elves)):
		elves[i] = (elves[i] + recipeScores[elves[i]] + 1) % len(recipeScores)
	return len(scoreSumAsString)

# Returns True iff for each element in subList we can find an equal element in fullList.
# The entire list subList will be compared against fullList, starting at index "offset" in fullList.
def matchSubList(fullList, subList, offset):
	if len(fullList) < len(subList) or offset < 0:
		return False
	for i in range(len(subList)):
		if fullList[offset+i] != subList[i]:
			return False
	return True

########
# Main #
########
recipeScores = [3, 7]
elves = [0, 1]
puzzleInput = "440231"
answerSizePart1 = 10

print("Part 1: {}".format(part1(recipeScores, elves, int(puzzleInput), answerSizePart1)))
print("Part 2: {}".format(part2(recipeScores, elves, [int(x) for x in puzzleInput])))
