import re

###########
# Classes #
###########
class MarbleGame:
	def __init__(self, numberOfPlayers):
		self.marbles = [0]
		self.currentMarbleIndex = 0
		self.valueOfNextMarble = 1
		self.numberOfPlayers = numberOfPlayers
		self.currentPlayerIndex = 0
		self.playerToScore = {}
		for i in range(numberOfPlayers):
			self.playerToScore[i] = 0

	def playNextMarble(self):
		if self.valueOfNextMarble % 23 == 0:
			# Special case for multiples of 23
			self.currentMarbleIndex = (self.currentMarbleIndex-7) % len(self.marbles)
			self.playerToScore[self.currentPlayerIndex] += self.valueOfNextMarble
			self.playerToScore[self.currentPlayerIndex] += self.marbles[self.currentMarbleIndex]
			self.marbles.pop(self.currentMarbleIndex)
		else:
			self.currentMarbleIndex = (self.currentMarbleIndex+2) % len(self.marbles)
			self.marbles.insert(self.currentMarbleIndex, self.valueOfNextMarble)
		self.valueOfNextMarble += 1
		self.currentPlayerIndex = (self.currentPlayerIndex+1) % self.numberOfPlayers

#############
# Functions #
#############
# Reads a file, and returns (numberOfPlayers, lastMarble), where:
# - numberOfPlayers is the number of players.
# - lastMarble is the value of the last marble.
def getGameParametersFromFile(fileName):
	with open(fileName) as f:
		text = f.read().strip()
		match = re.match("(\d+) players; last marble is worth (\d+) points", text)
		if match:
			numberOfPlayers = int(match.group(1))
			lastMarble = int(match.group(2))
		else:
			raise ValueError("File has invalid format: {}".format(text))
	return (numberOfPlayers, lastMarble)

########
# Main #
########
(numberOfPlayers, lastMarble) = getGameParametersFromFile("input09")
print("Number of players: {}".format(numberOfPlayers))
print("Value of last marble: {}".format(lastMarble))
marbleGame = MarbleGame(numberOfPlayers)
while marbleGame.valueOfNextMarble <= lastMarble:
	marbleGame.playNextMarble()
(playerIndex, score) = sorted(marbleGame.playerToScore.items(), key=lambda item: item[1], reverse=True)[0]
print("Player {player} wins with {score} points".format(player=playerIndex+1, score=score))

marbleGame = MarbleGame(numberOfPlayers)
while marbleGame.valueOfNextMarble <= lastMarble*100:
	marbleGame.playNextMarble()
	if marbleGame.valueOfNextMarble % 100000 == 0:
		print("Next marble is worth {} points".format(marbleGame.valueOfNextMarble), flush=True)
(playerIndex, score) = sorted(marbleGame.playerToScore.items(), key=lambda item: item[1], reverse=True)[0]
print("Player {player} wins with {score} points".format(player=playerIndex+1, score=score))
