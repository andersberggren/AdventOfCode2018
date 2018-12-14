#############
# Functions #
#############
def part1(recipeScores, elfA, elfB, numberOfRecipes):
	while len(recipeScores) < numberOfRecipes+10:
		scoreSum = recipeScores[elfA] + recipeScores[elfB]
		# Add new recipe scores
		for digitAsString in str(scoreSum):
			recipeScores.append(int(digitAsString))
		# Move elf index
		elfA = (elfA + recipeScores[elfA] + 1) % len(recipeScores)
		elfB = (elfB + recipeScores[elfB] + 1) % len(recipeScores)

	# Get the 10 last scores
	finalScore = ""
	for i in range(numberOfRecipes, numberOfRecipes+10):
		finalScore += str(recipeScores[i])
	print("Final score: {}".format(finalScore))

def part2(recipeScores, elfA, elfB, digitSequence):
	print("Digits for part 2: {}".format(digitSequence))
	print("Recipe scores: {}".format(recipeScores))
	while True:
		scoreSum = recipeScores[elfA] + recipeScores[elfB]
		# Add new recipe scores
		for digitAsString in str(scoreSum):
			recipeScores.append(int(digitAsString))
			if areLastDigitsTheSame(recipeScores, digitSequence):
				print("Part 2: {}".format(len(recipeScores) - len(digitSequence)))
				return
			if len(recipeScores) % 100000 == 0:
				print("{: >11,} recipes created".format(len(recipeScores)), flush=True)
		# Move elf index
		elfA = (elfA + recipeScores[elfA] + 1) % len(recipeScores)
		elfB = (elfB + recipeScores[elfB] + 1) % len(recipeScores)

def areLastDigitsTheSame(recipeScores, digitSequence):
	if len(recipeScores) < len(digitSequence):
		return False
	offset = len(recipeScores) - len(digitSequence)
	for i in range(len(digitSequence)):
		if recipeScores[offset+i] != digitSequence[i]:
			return False
	return True

########
# Main #
########
recipeScores = [3, 7]
elfA = 0
elfB = 1
target = "440231"
part1(recipeScores, elfA, elfB, int(target))

recipeScores = [3, 7]
part2(recipeScores, elfA, elfB, [int(digitAsString) for digitAsString in target])
