########
# Main #
########
recipeScores = [3, 7]
elfA = 0
elfB = 1
numberOfRecipes = 440231

while len(recipeScores) < numberOfRecipes+10:
	scoreSum = recipeScores[elfA] + recipeScores[elfB]
	# Add new recipe scores
	for digitAsString in str(scoreSum):
		recipeScores.append(int(digitAsString))
	#print("Recipe scores: {}".format(recipeScores))
	# Move elf index
	elfA = (elfA + recipeScores[elfA] + 1) % len(recipeScores)
	elfB = (elfB + recipeScores[elfB] + 1) % len(recipeScores)

# Get the 10 last scores
finalScore = ""
for i in range(numberOfRecipes, numberOfRecipes+10):
	finalScore += str(recipeScores[i])
print("Final score: {}".format(finalScore))
