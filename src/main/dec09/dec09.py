import re

from aoclib.circularlist import CircularList

###########
# Classes #
###########
class MarbleGame:
	def __init__(self, numberOfPlayers, valueOfFinalMarble):
		self.marbles = CircularList()
		self.marbles.insert(0)
		self.valueOfNextMarble = 1
		self.valueOfFinalMarble = valueOfFinalMarble
		self.numberOfPlayers = numberOfPlayers
		self.currentPlayerIndex = 0
		# Dict, from player index (starting at 0), to the players score
		self.playerToScore = {}
		for i in range(numberOfPlayers):
			self.playerToScore[i] = 0

	def playGame(self):
		while self.valueOfNextMarble <= self.valueOfFinalMarble:
			self.playNextMarble()
		(playerIndex, score) = sorted(self.playerToScore.items(), key=lambda item: item[1], reverse=True)[0]
		# Add 1 to playerIndex.
		# Internally, index starts at 0, but the answer expects index to start at 1
		return (playerIndex+1, score)

	def playNextMarble(self):
		if self.valueOfNextMarble % 23 == 0:
			# Special case for multiples of 23
			self.marbles.moveCursor(-7)
			self.playerToScore[self.currentPlayerIndex] += self.valueOfNextMarble
			self.playerToScore[self.currentPlayerIndex] += self.marbles.remove()
		else:
			self.marbles.moveCursor(2)
			self.marbles.insert(self.valueOfNextMarble)
		self.valueOfNextMarble += 1
		self.currentPlayerIndex = (self.currentPlayerIndex+1) % self.numberOfPlayers

#############
# Functions #
#############
# Reads a file, and returns (numberOfPlayers, valueOfFinalMarble), where:
# - numberOfPlayers is the number of players.
# - valueOfFinalMarble is the value of the final marble in the game.
def getGameParametersFromFile(fileName):
	with open(fileName) as f:
		text = f.read().strip()
		match = re.match("(\d+) players; last marble is worth (\d+) points", text)
		if match:
			numberOfPlayers = int(match.group(1))
			valueOfFinalMarble = int(match.group(2))
		else:
			raise ValueError("File has invalid format: {}".format(text))
	return (numberOfPlayers, valueOfFinalMarble)

########
# Main #
########
(numberOfPlayers, valueOfFinalMarble) = getGameParametersFromFile("input09.txt")

# Part 1
(winningPlayer, score) = MarbleGame(numberOfPlayers, valueOfFinalMarble).playGame()
print("Part 1: Player {player} wins with {score} points".format(player=winningPlayer, score=score))

# Part 2
(winningPlayer, score) = MarbleGame(numberOfPlayers, valueOfFinalMarble*100).playGame()
print("Part 2: Player {player} wins with {score} points".format(player=winningPlayer, score=score))
