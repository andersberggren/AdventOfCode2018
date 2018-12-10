import re

###########
# Classes #
###########
# A circular linked list.
class LinkedList:
	def __init__(self):
		self.currentItem = None
		self.size = 0

	# Inserts "value" before the current item.
	# The inserted item then becomes the current item.
	def add(self, value):
		newItem = LinkedListItem(value)
		if self.size == 0:
			newItem.prev = newItem
			newItem.next = newItem
		else:
			itemBefore = self.currentItem.prev
			itemBefore.next = newItem
			self.currentItem.prev = newItem
			newItem.next = self.currentItem
			newItem.prev = itemBefore
		self.currentItem = newItem
		self.size += 1

	# Removes the current item from the list, and returns it.
	# The next item in the list becomes the current item.
	def remove(self):
		if self.size == 0:
			raise RuntimeError("Can't remove, size is 0")
		valueToReturn = self.currentItem.value
		if self.size == 1:
			self.currentItem = None
		else:
			itemBefore = self.currentItem.prev
			itemAfter = self.currentItem.next
			itemBefore.next = itemAfter
			itemAfter.prev = itemBefore
			self.currentItem = itemAfter
		self.size -= 1
		return valueToReturn

	# Returns the current item.
	def get(self):
		return self.currentItem.value

	# Moves the "current item"-pointer forwards "steps" number of steps.
	def forward(self, steps):
		for i in range(steps):
			self.currentItem = self.currentItem.next

	# Moves the "current item"-pointer backwards "steps" number of steps.
	def backward(self, steps):
		for i in range(steps):
			self.currentItem = self.currentItem.prev

class LinkedListItem:
	def __init__(self, value):
		self.prev = None
		self.next = None
		self.value = value

class MarbleGame:
	def __init__(self, numberOfPlayers):
		self.marbles = LinkedList()
		self.marbles.add(0)
		self.valueOfNextMarble = 1
		self.numberOfPlayers = numberOfPlayers
		self.currentPlayerIndex = 0
		# Dict, from player index (starting at 0), to the players score
		self.playerToScore = {}
		for i in range(numberOfPlayers):
			self.playerToScore[i] = 0

	def playNextMarble(self):
		if self.valueOfNextMarble % 23 == 0:
			# Special case for multiples of 23
			self.marbles.backward(7)
			self.playerToScore[self.currentPlayerIndex] += self.valueOfNextMarble
			self.playerToScore[self.currentPlayerIndex] += self.marbles.get()
			self.marbles.remove()
		else:
			self.marbles.forward(2)
			self.marbles.add(self.valueOfNextMarble)
		self.valueOfNextMarble += 1
		self.currentPlayerIndex = (self.currentPlayerIndex+1) % self.numberOfPlayers

	def playGame(self, valueOfFinalMarble):
		while self.valueOfNextMarble <= valueOfFinalMarble:
			self.playNextMarble()
		(playerIndex, score) = sorted(self.playerToScore.items(), key=lambda item: item[1], reverse=True)[0]
		# Add 1 to playerIndex.
		# Internally, index starts at 0, but the answer expects index to start at 1
		return (playerIndex+1, score)

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
(numberOfPlayers, valueOfFinalMarble) = getGameParametersFromFile("input09")

# Part 1
marbleGame = MarbleGame(numberOfPlayers)
(winningPlayer, score) = marbleGame.playGame(valueOfFinalMarble)
print("Part 1: Player {player} wins with {score} points".format(player=winningPlayer, score=score))

# Part 2
marbleGame = MarbleGame(numberOfPlayers)
(winningPlayer, score) = marbleGame.playGame(valueOfFinalMarble*100)
print("Part 2: Player {player} wins with {score} points".format(player=winningPlayer, score=score))
