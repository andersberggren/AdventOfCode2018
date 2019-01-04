from aoclib.direction import Direction
from dec20.regex import getRegexWithinParentheses, splitRegexOnBranches

class Facility:
	startLocation = (0,0)
	symbolToDirection = {
		"N": Direction.up,
		"S": Direction.down,
		"E": Direction.right,
		"W": Direction.left
	}
	
	def __init__(self):
		# Dict. Key is room location (x,y). Value is Room object.
		self.locationToRoom = {}
		self.addRoom(Facility.startLocation)

	def addRoom(self, location):
		if location not in self.locationToRoom:
			self.locationToRoom[location] = Room(location)

	def addDoor(self, roomLocation, direction):
		"""
		Adds a door from room at "roomLocation" in direction "direction".
		Also adds the neighboring room if it doesn't already exist.
		"""
		room = self.locationToRoom[roomLocation]
		otherRoomLocation = Direction.getNewLocation(roomLocation, direction)
		if otherRoomLocation not in self.locationToRoom:
			self.locationToRoom[otherRoomLocation] = Room(otherRoomLocation)
		otherRoom = self.locationToRoom[otherRoomLocation]
		room.addConnection(otherRoom)

	def exploreFacilityAccordingToRegex(self, regex, locations=None):
		"""
		Arguments:
		  regex      Remaining regex.
		  locations  A set of locations, where we are currently at.
		Returns a set of locations, where we are at after exploring the regex.
		"""
		if locations is None:
			locations = {Facility.startLocation}
		if len(regex) == 0:
			return locations
		regexList = splitRegexOnBranches(regex)
		if len(regexList) > 1:
			# Recursive call for each branch
			newLocations = set()
			for regexSection in regexList:
				newLocations |= self.exploreFacilityAccordingToRegex(regexSection, locations)
			return newLocations
		else:
			# Single branch
			if regex[0] == "(":
				(regexWithinParentheses, regexTail) = getRegexWithinParentheses(regex)
				locations = self.exploreFacilityAccordingToRegex(regexWithinParentheses, locations)
				return self.exploreFacilityAccordingToRegex(regexTail, locations)
			else:
				# Evaluate one symbol at a time, until "("
				for i in range(len(regex)):
					symbol = regex[i]
					if symbol in Facility.symbolToDirection:
						direction = Facility.symbolToDirection[symbol]
						newLocations = set()
						for location in locations:
							self.addDoor(location, direction)
							newLocations.add(Direction.getNewLocation(location, direction))
						locations = newLocations
					elif symbol == "(":
						return self.exploreFacilityAccordingToRegex(regex[i:], locations)
					else:
						raise RuntimeError("Unexpected symbol: {}".format(symbol))
				return locations

	def getShortestDistanceToEveryRoom(self):
		""" Returns a dict, where key is room, and value is shortest distance to room. """
		roomToDistance = {}
		startRoom = self.locationToRoom[Facility.startLocation]
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
	def __init__(self, location):
		self.location = location
		self.connectedRooms = set()

	def addConnection(self, otherRoom):
		self.connectedRooms.add(otherRoom)
		otherRoom.connectedRooms.add(self)
