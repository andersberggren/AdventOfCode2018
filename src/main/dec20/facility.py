from aoclib.direction import Direction
class Facility:
	symbolToDirection = {
		"N": Direction.up,
		"S": Direction.down,
		"E": Direction.right,
		"W": Direction.left
	}
	
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

	# Returns a dict, where key is room, and value is shortest distance to room.
	def getShortestDistanceToEveryRoom(self):
		roomToDistance = {}
		startRoom = self.positionToRoom[(0,0)]
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
