# Returns the manhattan distance between two 2-dimensional coordinates.
def getManhattanDistance2(coordinateA, coordinateB):
	return abs(coordinateA[0]-coordinateB[0]) \
			+ abs(coordinateA[1]-coordinateB[1])

# Returns the manhattan distance between two 3-dimensional coordinates.
def getManhattanDistance3(coordinateA, coordinateB):
	return abs(coordinateA[0]-coordinateB[0]) \
			+ abs(coordinateA[1]-coordinateB[1]) \
			+ abs(coordinateA[2]-coordinateB[2])

# Returns the manhattan distance between two 4-dimensional coordinates.
def getManhattanDistance4(coordinateA, coordinateB):
	return abs(coordinateA[0]-coordinateB[0]) \
			+ abs(coordinateA[1]-coordinateB[1]) \
			+ abs(coordinateA[2]-coordinateB[2]) \
			+ abs(coordinateA[3]-coordinateB[3])
