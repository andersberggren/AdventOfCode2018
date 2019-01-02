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

def getManhattanDistance3FromBox(boxLocation, boxSize, pointLocation):
	"""
	Returns the manhattan distance between a box and a point.
	The distance returned is the shortest distance from any point in the box.
	Arguments:
	  boxLocation    The corner of the box with the smallest (x,y,z).
	  boxSize        The size of the box.
	  pointLocation  The location to measure distance to.
	"""
	distance = 0
	for i in range(3):
		minValue = boxLocation[i]
		maxValue = boxLocation[i]+boxSize[i]-1
		distance += max(pointLocation[i] - maxValue, minValue - pointLocation[i], 0)
	return distance

def getBoundingBox(locations):
	"""
	Returns (location, size) of the smallest bounding box containing all the locations
	in "locations". "location" and "size" are 3-tuples.
	"""
	minValues = [min(x[i] for x in locations) for i in range(3)]
	maxValues = [max(x[i] for x in locations) for i in range(3)]
	location = tuple(minValues)
	size = tuple(maxValues[i]-minValues[i]+1 for i in range(3))
	return (location, size)

def getSubBoxes(boxLocation, boxSize):
	"""
	Returns a list of the (up to) 8 sub-boxes that results from splitting a box in half
	along all 3 dimensions. If a sub-box has a size is 0 along at least one dimension,
	that sub-box is not included in the result.
	Arguments:
	  boxLocation  The corner of the box with the smallest (x,y,z)
	  boxSize      The size of the box
	"""
	newSizes = [[boxSize[i]//2, boxSize[i] - (boxSize[i]//2)] for i in range(3)]
	newLocations = [[boxLocation[i], boxLocation[i]+newSizes[i][0]] for i in range(3)]
	subBoxes = []
	for x in range(2):
		for y in range(2):
			for z in range(2):
				newLocation  = (newLocations[0][x], newLocations[1][y], newLocations[2][z])
				newSize = (newSizes[0][x],     newSizes[1][y],     newSizes[2][z])
				if all([s >= 1 for s in newSize]):
					subBoxes.append((newLocation, newSize))
	return subBoxes
