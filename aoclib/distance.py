def getManhattanDistance2(coordinateA, coordinateB):
	""" Returns the manhattan distance between two 2-dimensional coordinates. """
	return abs(coordinateA[0]-coordinateB[0]) + abs(coordinateA[1]-coordinateB[1])

def getManhattanDistance3(coordinateA, coordinateB):
	""" Returns the manhattan distance between two 3-dimensional coordinates. """
	return abs(coordinateA[0]-coordinateB[0]) + abs(coordinateA[1]-coordinateB[1]) \
			+ abs(coordinateA[2]-coordinateB[2])

def getManhattanDistance4(coordinateA, coordinateB):
	""" Returns the manhattan distance between two 4-dimensional coordinates. """
	return abs(coordinateA[0]-coordinateB[0]) + abs(coordinateA[1]-coordinateB[1]) \
			+ abs(coordinateA[2]-coordinateB[2]) + abs(coordinateA[3]-coordinateB[3])

def getManhattanDistance3FromCuboid(cuboidCoordinate, cuboidSize, coordinate):
	"""
	Returns the manhattan distance between a (rectangular) cuboid and a 3-dimensional coordinate.
	The distance returned is the shortest from any point in the cuboid.
	Arguments:
	  cuboidCoordinate  The corner of the cuboid with the smallest (x,y,z)
	  cuboidSize        The size of the cuboid
	  coordinate        The coordinate to measure distance to
	"""
	distance = 0
	for i in range(3):
		minValue = cuboidCoordinate[i]
		maxValue = cuboidCoordinate[i]+cuboidSize[i]-1
		distance += max(coordinate[i] - maxValue, minValue - coordinate[i], 0)
	return distance
