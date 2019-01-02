###########
# Classes #
###########
class Facility:
	def __init__(self):
		# Dict. Key is room position (x,y). Value is Room object.
		self.positionToRoom = {}
		self.addRoom((0,0))

	def addRoom(self, position):
		if position not in self.positionToRoom:
			self.positionToRoom[position] = Room(position)

	# Adds a door from room at "roomPosition" in direction "direction".
	# Also adds the neighboring room if it doesn't already exist.
	def addDoor(self, roomPosition, direction):
		room = self.positionToRoom[roomPosition]
		otherRoomPosition = (roomPosition[0]+direction[0], roomPosition[1]+direction[1])
		if otherRoomPosition not in self.positionToRoom:
			self.positionToRoom[otherRoomPosition] = Room(otherRoomPosition)
		otherRoom = self.positionToRoom[otherRoomPosition]
		room.addConnection(otherRoom)

class Room:
	def __init__(self, position):
		self.position = position
		self.connectedRooms = set()

	def addConnection(self, otherRoom):
		self.connectedRooms.add(otherRoom)
		otherRoom.connectedRooms.add(self)

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
# Returns a set of positions, where we are at after exploring the regex.
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
						facility.addDoor(position, direction)
						newPositions.add((position[0]+direction[0], position[1]+direction[1]))
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

# Returns a dict, where key is room, and value is shortest distance to room.
def getShortestDistanceToEveryRoom(facility):
	roomToDistance = {}
	startRoom = facility.positionToRoom[(0,0)]
	visitedRooms = set([startRoom])
	fringe = set([startRoom])
	currentDistance = 0
	while len(fringe) > 0:
		for room in fringe:
			roomToDistance[room] = currentDistance
		fringe = set(r2 for r in fringe for r2 in r.connectedRooms if r2 not in visitedRooms)
		visitedRooms |= fringe
		currentDistance += 1
	return roomToDistance

########
# Main #
########
if __name__ == "__main__":
	facility = Facility()
	regex = readRegexFromFile("input20.txt")
	positions = set([(0,0)])
	exploreFacilityAccordingToRegex(facility, regex, positions)
	roomToDistance = getShortestDistanceToEveryRoom(facility)
	# Part 1
	maxDistance = max(x for x in roomToDistance.values())
	print("Shortest distance to most distant room: {}".format(maxDistance))
	# Part 2
	numberOfRooms = len([x for x in roomToDistance.values() if x >= 1000])
	print("Number of rooms requiring passing through at least 1000 doors: {}".format(numberOfRooms))
