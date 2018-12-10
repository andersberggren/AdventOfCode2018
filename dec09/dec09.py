import re

###########
# Classes #
###########
# A circular and doubly-linked list.
class LinkedList:
	def __init__(self):
		self.cursor = None
		self.size = 0

	# Inserts "valueToInsert" before the cursor.
	# After insert, the cursor points to the new element.
	def add(self, valueToInsert):
		newElement = LinkedList.Element(valueToInsert)
		if self.size == 0:
			newElement.prev = newElement
			newElement.next = newElement
		else:
			prevElement = self.cursor.prev
			prevElement.next = newElement
			self.cursor.prev = newElement
			newElement.next = self.cursor
			newElement.prev = prevElement
		self.cursor = newElement
		self.size += 1

	# Removes the element at the cursor, and returns the element.
	# After remove, the cursor points to the element after the element that was removed.
	def remove(self):
		if self.size == 0:
			raise RuntimeError("Can't remove, size is 0")
		valueToReturn = self.cursor.value
		if self.size == 1:
			self.cursor = None
		else:
			prevElement = self.cursor.prev
			nextElement = self.cursor.next
			prevElement.next = nextElement
			nextElement.prev = prevElement
			self.cursor = nextElement
		self.size -= 1
		return valueToReturn

	# Returns the element at the cursor.
	def get(self):
		return self.cursor.value

	# Moves the cursor "numberOfSteps" steps (can be negative).
	def moveCursor(self, numberOfSteps):
		while numberOfSteps != 0:
			if numberOfSteps < 0:
				self.cursor = self.cursor.prev
				numberOfSteps += 1
			elif numberOfSteps > 0:
				self.cursor = self.cursor.next
				numberOfSteps -= 1

	# An element in the list, with references to the previous and next element in the list.
	class Element:
		def __init__(self, value):
			self.value = value
			self.prev = None
			self.next = None

class MarbleGame:
	def __init__(self, numberOfPlayers, valueOfFinalMarble):
		self.marbles = LinkedList()
		self.marbles.add(0)
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
			self.marbles.add(self.valueOfNextMarble)
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
(numberOfPlayers, valueOfFinalMarble) = getGameParametersFromFile("input09")

# Part 1
(winningPlayer, score) = MarbleGame(numberOfPlayers, valueOfFinalMarble).playGame()
print("Part 1: Player {player} wins with {score} points".format(player=winningPlayer, score=score))

# Part 2
(winningPlayer, score) = MarbleGame(numberOfPlayers, valueOfFinalMarble*100).playGame()
print("Part 2: Player {player} wins with {score} points".format(player=winningPlayer, score=score))
