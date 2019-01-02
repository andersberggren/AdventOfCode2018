#########
# Class #
#########
class ChocolateLaboratory:
	def __init__(self):
		self.recipeScores = [3, 7]
		self.elves = [0, 1]

	# Appends new recipe scores (one or two) at the end of recipeScores,
	# and updates which recipes the elves are at.
	# Returns the number of recipe scores added.
	def update(self):
		scoreSumAsString = str(sum([self.recipeScores[elf] for elf in self.elves]))
		self.recipeScores.extend([int(digitAsString) for digitAsString in scoreSumAsString])
		self.elves = [(elf+self.recipeScores[elf]+1) % len(self.recipeScores) for elf in self.elves]
		return len(scoreSumAsString)

#############
# Functions #
#############
# Arguments:
#   lab              The chocolate laboratory
#   numberOfRecipes  The number of recipe scores to generate, before the answer.
#   answerSize       The number of recipe scores, after numberOfRecipes, for the answer.
#
# Returns a string with the answerSize digits that follows immediately after
# generating numberOfRecipes recipes.
def part1(lab, numberOfRecipes, answerSize):
	while len(lab.recipeScores) < numberOfRecipes+answerSize:
		lab.update()
	return "".join([str(d) for d in lab.recipeScores[numberOfRecipes:numberOfRecipes+answerSize]])

# Arguments:
#   lab            The chocolate laboratory
#   digitSequence  A list of integers. This is the sequence of digits we look for in recipeScores.
#
# Returns the number of recipe scores that need to be generated,
# before the digit sequence in digitSequence occurs in the recipe scores.
def part2(lab, digitSequence):
	while True:
		numberOfNewScores = lab.update()
		for i in range(numberOfNewScores):
			offset = len(lab.recipeScores) - len(digitSequence) - (numberOfNewScores-1) + i
			if offset >= 0 and matchSubList(lab.recipeScores, digitSequence, offset):
				return offset
		if (len(lab.recipeScores) % 1000000) - numberOfNewScores < 0:
			print("{: >11,} recipes created".format(len(lab.recipeScores)), flush=True)

# Returns True iff for each element in subList we can find an equal element at the corresponding
# index in fullList. The entire list subList will be compared against fullList, starting at index
# "offset" in fullList.
def matchSubList(fullList, subList, offset):
	for i in range(len(subList)):
		if fullList[offset+i] != subList[i]:
			return False
	return True

########
# Main #
########
if __name__ == "__main__":
	puzzleInput = "440231"
	answerSizePart1 = 10
	answer1 = part1(ChocolateLaboratory(), int(puzzleInput), answerSizePart1)
	print("Part 1. Digit sequence after {n} recipes: {a}".format(n=puzzleInput, a=answer1))
	answer2 = part2(ChocolateLaboratory(), [int(x) for x in puzzleInput])
	print("Part 2. Digit sequence occurs after {} recipes".format(answer2))
