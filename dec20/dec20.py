###########
# Classes #
###########
class Facility:
	def __init__(self):
		# Dict, where key is room position (x,y), and value is Room object.
		self.positionToRoom = {}
		self.addRoom((0,0))

	def addRoom(self, position):
		if position not in self.positionToRoom:
			self.positionToRoom[position] = Room(position)

	def addDoor(self, position, direction):
		roomA = self.positionToRoom[position]
		roomB = self.positionToRoom[(position[0]+direction[0], position[1]+direction[1])]
		roomA.addConnection(roomB)
		roomB.addConnection(roomA)

class Room:
	def __init__(self, position):
		self.position = position
		self.connectedRooms = set()

	def addConnection(self, otherRoom):
		direction = (otherRoom.position[0]-self.position[0], otherRoom.position[1]-self.position[1])
		if direction not in Direction.all:
			raise RuntimeError("Invalid connection from room at {p1} to room at {p2}".format(
					p1=self.position, p2=otherRoom.position))
		self.connectedRooms.add(otherRoom)

class Direction:
	north = ( 0, -1)
	south = ( 0,  1)
	east =  ( 1,  0)
	west =  (-1,  0)
	all = set([north, south, east, west])

	@staticmethod
	def getDirectionFromSymbol(symbol):
		if symbol == "N":
			return Direction.north
		elif symbol == "S":
			return Direction.south
		elif symbol == "E":
			return Direction.east
		elif symbol == "W":
			return Direction.west
		else:
			raise ValueError("Invalid symbol: {}".format(symbol))

#############
# Functions #
#############
def readRegexFromFile(fileName):
	with open(fileName) as f:
		return f.read().lstrip("^").rstrip().rstrip("$")

# Arguments:
#   facility   The facility to explore.
#   regex      Remaining regex.
#   positions  A set of positions, where we are currently at.
def exploreFacilityAccordingToRegex(facility, regex, positions):
	if len(regex) == 0:
		return positions
	regexList = splitRegexOnBranches(regex)
	if len(regexList) > 1:
		# Recursive call for each branch
		newPositions = set()
		for regexSection in regexList:
			newPositions |= exploreFacilityAccordingToRegex(facility, regexSection, positions)
		return newPositions
	else:
		# Single branch
		if regex[0] == "(":
			(regexWithinParentheses, regexTail) = getRegexWithinParentheses(regex)
			positions = exploreFacilityAccordingToRegex(facility, regexWithinParentheses, positions)
			return exploreFacilityAccordingToRegex(facility, regexTail, positions)
		else:
			# Evaluate one symbol at a time, until "("
			for i in range(len(regex)):
				symbol = regex[i]
				if symbol in ["N", "S", "E", "W"]:
					direction = Direction.getDirectionFromSymbol(symbol)
					newPositions = set()
					for position in positions:
						newPosition = (position[0]+direction[0], position[1]+direction[1])
						newPositions.add(newPosition)
						facility.addRoom(newPosition)
						facility.addDoor(position, direction)
					positions = newPositions
				elif symbol == "(":
					return exploreFacilityAccordingToRegex(facility, regex[i:], positions)
				else:
					raise RuntimeError("Unexpected symbol: {}".format(symbol))
			return positions

# Returns (regexWithinParentheses, regexTail)
def getRegexWithinParentheses(regex):
	if regex[0] != "(":
		raise RuntimeError("Expected regex to start with \"(\", but was \"{}\"".format(regex[0]))
	# "balance" is number of "(" minus number of ")"
	balance = 1
	i = 1
	while balance > 0:
		if regex[i] == "(":
			balance += 1
		elif regex[i] == ")":
			balance -= 1
		i += 1
	regexWithinParentheses = regex[1:i-1]
	regexTail = regex[i:]
	return (regexWithinParentheses, regexTail)

# Returns a list of regex
def splitRegexOnBranches(regex):
	regexList = []
	balance = 0
	i = 0
	while i < len(regex):
		if regex[i] == "|" and balance == 0:
			regexList.append(regex[:i])
			regex = regex[i+1:]
			i = 0
		else:
			if regex[i] == "(":
				balance += 1
			elif regex[i] == ")":
				balance -= 1
			i += 1
	regexList.append(regex)
	return regexList

def getDistanceToMostDistantRoom(facility):
	startRoom = facility.positionToRoom[(0,0)]
	visitedRooms = set([startRoom])
	fringe = set([startRoom])
	distance = 0
	while len(fringe) > 0:
		newFringe = set()
		for room in fringe:
			for nextRoom in room.connectedRooms:
				if nextRoom not in visitedRooms:
					visitedRooms.add(nextRoom)
					newFringe.add(nextRoom)
		fringe = newFringe
		if len(fringe) > 0:
			distance += 1
	return distance

########
# Main #
########
if __name__ == "__main__":
	facility = Facility()
	regex = readRegexFromFile("input20")
	positions = set([(0,0)])
	exploreFacilityAccordingToRegex(facility, regex, positions)
	print("Number of rooms: {}".format(len(facility.positionToRoom)))
	print("Shortest distance to most distant room: {}".format(
		getDistanceToMostDistantRoom(facility)))

