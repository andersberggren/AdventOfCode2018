from aoclib.direction import Direction
from dec20.regex import getRegexWithinParentheses, splitRegexOnBranches

class Facility:
	startPosition = (0,0)
	symbolToDirection = {
		"N": Direction.up,
		"S": Direction.down,
		"E": Direction.right,
		"W": Direction.left
	}
	
	def __init__(self):
		# Dict. Key is room position (x,y). Value is Room object.
		self.positionToRoom = {}
		self.addRoom(Facility.startPosition)

	def addRoom(self, position):
		if position not in self.positionToRoom:
			self.positionToRoom[position] = Room(position)

	def addDoor(self, roomPosition, direction):
		"""
		Adds a door from room at "roomPosition" in direction "direction".
		Also adds the neighboring room if it doesn't already exist.
		"""
		room = self.positionToRoom[roomPosition]
		otherRoomPosition = Direction.getNewLocation(roomPosition, direction)
		if otherRoomPosition not in self.positionToRoom:
			self.positionToRoom[otherRoomPosition] = Room(otherRoomPosition)
		otherRoom = self.positionToRoom[otherRoomPosition]
		room.addConnection(otherRoom)

	def exploreFacilityAccordingToRegex(self, regex, positions=None):
		"""
		Arguments:
		  regex      Remaining regex.
		  positions  A set of positions, where we are currently at.
		Returns a set of positions, where we are at after exploring the regex.
		"""
		if positions is None:
			positions = {Facility.startPosition}
		if len(regex) == 0:
			return positions
		regexList = splitRegexOnBranches(regex)
		if len(regexList) > 1:
			# Recursive call for each branch
			newPositions = set()
			for regexSection in regexList:
				newPositions |= self.exploreFacilityAccordingToRegex(regexSection, positions)
			return newPositions
		else:
			# Single branch
			if regex[0] == "(":
				(regexWithinParentheses, regexTail) = getRegexWithinParentheses(regex)
				positions = self.exploreFacilityAccordingToRegex(regexWithinParentheses, positions)
				return self.exploreFacilityAccordingToRegex(regexTail, positions)
			else:
				# Evaluate one symbol at a time, until "("
				for i in range(len(regex)):
					symbol = regex[i]
					if symbol in Facility.symbolToDirection:
						direction = Facility.symbolToDirection[symbol]
						newPositions = set()
						for position in positions:
							self.addDoor(position, direction)
							newPositions.add(Direction.getNewLocation(position, direction))
						positions = newPositions
					elif symbol == "(":
						return self.exploreFacilityAccordingToRegex(regex[i:], positions)
					else:
						raise RuntimeError("Unexpected symbol: {}".format(symbol))
				return positions

	def getShortestDistanceToEveryRoom(self):
		""" Returns a dict, where key is room, and value is shortest distance to room. """
		roomToDistance = {}
		startRoom = self.positionToRoom[Facility.startPosition]
		visitedRooms = {startRoom}
		fringe = {startRoom}
		currentDistance = 0
		while len(fringe) > 0:
			for room in fringe:
				roomToDistance[room] = currentDistance
			fringe = {r2 for r in fringe for r2 in r.connectedRooms if r2 not in visitedRooms}
			visitedRooms |= fringe
			currentDistance += 1
		return roomToDistance

class Room:
	def __init__(self, position):
		self.position = position
		self.connectedRooms = set()

	def addConnection(self, otherRoom):
		self.connectedRooms.add(otherRoom)
		otherRoom.connectedRooms.add(self)
