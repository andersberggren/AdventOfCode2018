###########
# Classes #
###########
class PointOfInterest:
	nextId = 0

	def __init__(self, id, x, y):
		self.id = id
		self.x = int(x)
		self.y = int(y)

	@staticmethod
	def createFromString(s):
		id = PointOfInterest.nextId
		PointOfInterest.nextId += 1
		x = s.split(",")[0].strip()
		y = s.split(",")[1].strip()
		return PointOfInterest(id, x, y)

class Grid:
	def __init__(self, poiSet):
		self.minX = min([poi.x for poi in poiSet])
		self.maxX = max([poi.x for poi in poiSet])
		self.minY = min([poi.y for poi in poiSet])
		self.maxY = max([poi.y for poi in poiSet])
		self.poiSet = poiSet
		# coordToClosestPOI is a map, where the key is the (x,y)-coordinate, and
		# the value is the closest POI or None if two or more POIs are tied for closest.
		self.coordToClosestPOI = {}
		for x in self.getXRange():
			for y in self.getYRange():
				self.coordToClosestPOI[(x,y)] = self.getClosestPointOfInterest(x, y)

	# Returns the closest POI, or None if two or more POIs are tied for closest.
	def getClosestPointOfInterest(self, x, y):
		minDistance = None
		closestPOI = None
		for poi in self.poiSet:
			distance = getManhattanDistance((x,y), (poi.x,poi.y))
			if minDistance is None or distance < minDistance:
				minDistance = distance
				closestPOI = poi
			elif distance == minDistance:
				closestPOI = None
		return closestPOI

	# Finds the largest non-infinite area and returns a tuple: (PointOfInterest, area size)
	def findLargestNonInfiniteArea(self):
		poiSetNonInfinite = self.getPointsOfInterestWithNonInfiniteArea()
		poiToAreaSize = {}
		for items in self.coordToClosestPOI.items():
			(x, y) = items[0]
			closestPOI = items[1]
			if closestPOI in poiSetNonInfinite:
				try:
					poiToAreaSize[closestPOI] += 1
				except KeyError:
					poiToAreaSize[closestPOI] = 1
		return sorted(poiToAreaSize.items(), key=lambda item: item[1], reverse=True)[0]

	# Returns a set containing all POIs with non-infinite area.
	# A POI covers an infinite area if it is closest to any square on the edge of the grid.
	def getPointsOfInterestWithNonInfiniteArea(self):
		poiSetNonInfinite = set(self.poiSet)
		for coordinate in self.getEdgeCoordinates():
			closestPOI = self.coordToClosestPOI[coordinate]
			if closestPOI is not None and closestPOI in poiSetNonInfinite:
				poiSetNonInfinite.remove(closestPOI)
		return poiSetNonInfinite

	# Returns the number of squares where the total manhattan distance to all
	# POIs are less than maxTotalDistance.
	def getSizeOfAreaWithTotalDistanceLessThan(self, maxTotalDistance):
		areaSize = 0
		for (x, y) in self.getEdgeCoordinates():
			if self.getTotalDistance(x, y) < maxTotalDistance:
				raise RuntimeError("Unexpected: Coordinate on edge of grid satisfies the "
						+ "maxTotalDistance-condition. The implementation will probably not work.")
		for x in self.getXRange():
			for y in self.getYRange():
				if self.getTotalDistance(x, y) < maxTotalDistance:
					areaSize += 1
		return areaSize

	def getTotalDistance(self, x, y):
		totalDistance = 0
		for poi in self.poiSet:
			totalDistance += getManhattanDistance((x,y), (poi.x,poi.y))
		return totalDistance

	def getXRange(self):
		return range(self.minX, self.maxX+1)

	def getYRange(self):
		return range(self.minY, self.maxY+1)

	# Returns a list containing the (x,y)-coordinates of the grids edges.
	def getEdgeCoordinates(self):
		edgeCoordinates = [(x,y) for x in self.getXRange() for y in [self.minY, self.maxY]]
		edgeCoordinates.extend([(x,y) for x in [self.minX, self.maxX] for y in self.getYRange()])
		return list(set(edgeCoordinates))

#############
# Functions #
#############
def getPointsOfInterestFromFile(fileName):
	with open(fileName) as f:
		return set([PointOfInterest.createFromString(line) for line in f.readlines()])

def getManhattanDistance(coordinateA, coordinateB):
	return abs(coordinateA[0] - coordinateB[0]) + abs(coordinateA[1] - coordinateB[1])

########
# Main #
########
grid = Grid(getPointsOfInterestFromFile("input06"))

# Part 1
(poi, areaSize) = grid.findLargestNonInfiniteArea()
print("POI #{id} has the largest non-infinite area. Size is {size}".format(id=poi.id, size=areaSize))

# Part 2
maxTotalDistance = 10000
areaSize = grid.getSizeOfAreaWithTotalDistanceLessThan(10000)
print("Size of region with total distance to all POIs < {dist}: {size}".format(
		dist=maxTotalDistance,size=areaSize))
