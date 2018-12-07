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
		# TODO Is it necessary to specift PointOfInterest here?
		id = PointOfInterest.nextId
		PointOfInterest.nextId += 1
		x = s.split(",")[0].strip()
		y = s.split(",")[1].strip()
		return PointOfInterest(id, x, y)

#############
# Functions #
#############
def getPointsOfInterestFromFile(fileName):
	with open(fileName) as f:
		return set([PointOfInterest.createFromString(line) for line in f.readlines()])

# Returns a map where:
# - Key is a tuple with the (x,y)-coordinate
# - Value is the closest POI, or None if (x,y) is equally far from two or more POI.
def createGrid(poiSet):
	grid = {}
	minX = min([poi.x for poi in poiSet])
	maxX = max([poi.x for poi in poiSet])
	minY = min([poi.y for poi in poiSet])
	maxY = max([poi.y for poi in poiSet])
	for x in range(minX, maxX+1):
		for y in range(minY, maxY+1):
			grid[(x,y)] = getClosestPointOfInterest(x, y, poiSet)
	return grid

# Returns the closest POI, or None if two or more POIs are tied for closest.
def getClosestPointOfInterest(x, y, poiSet):
	minDistance = None
	closestPOI = None
	for poi in poiSet:
		distance = abs(x - poi.x) + abs(y - poi.y)
		if minDistance is None or distance < minDistance:
			minDistance = distance
			closestPOI = poi
		elif distance == minDistance:
			closestPOI = None
	return closestPOI

def getPointsOfInterestWithNonInfiniteAreas(grid, poiSet):
	# A POI covers an infinite area if it is closest to any square on the edge of the grid.
	poiSetNonInfinite = set(poiSet)
	minX = min([poi.x for poi in poiSet])
	maxX = max([poi.x for poi in poiSet])
	minY = min([poi.y for poi in poiSet])
	maxY = max([poi.y for poi in poiSet])
	coordinatesToCheck = [(x,y) for x in range(minX, maxX+1) for y in [minY, maxY]]
	coordinatesToCheck.extend([(x,y) for x in [minX, maxX] for y in range(minY, maxY+1)])
	for coordinate in coordinatesToCheck:
		closestPOI = grid[coordinate]
		if closestPOI is not None and closestPOI in poiSetNonInfinite:
			poiSetNonInfinite.remove(closestPOI)
	return poiSetNonInfinite

# Finds the largest non-infinite area and returns a tuple: (PointOfInterest, area size)
def findLargestNonInfiniteArea(grid, poiSetNonInfinite):
	# Map from POI to area size
	areaSizes = {}
	minX = min([x for (x,y) in grid])
	maxX = max([x for (x,y) in grid])
	minY = min([y for (x,y) in grid])
	maxY = max([y for (x,y) in grid])
	for items in grid.items():
		(x, y) = items[0]
		closestPOI = items[1]
		onEdge = x in [minX, maxX] or y in [minY, maxY]
		validPOI = closestPOI in poiSetNonInfinite
		if not onEdge and validPOI:
			try:
				areaSizes[closestPOI] += 1
			except KeyError:
				areaSizes[closestPOI] = 1
	return sorted(areaSizes.items(), key=lambda item: item[1], reverse=True)[0]

def getSizeOfAreaWithTotalDistanceLessThan(grid, poiSet, maxTotalDistance):
	areaSize = 0
	# TODO 4th copy-paste of this. Time to refactor and not repeat myself.
	minX = min([x for (x,y) in grid])
	maxX = max([x for (x,y) in grid])
	minY = min([y for (x,y) in grid])
	maxY = max([y for (x,y) in grid])
	for x in range(minX, maxX+1):
		for y in range(minY, maxY+1):
			if getTotalDistance(x, y, poiSet) < maxTotalDistance:
				areaSize += 1
				# TODO Don't repeat this "on edge"-condition.
				if x in [minX, maxX] or y in [minY, maxY]:
					raise RuntimeError("Unexpected: Coordinate on edge of grid satisfies maxTotalDistance-condition. The implementation will probably not work.")
	return areaSize

def getTotalDistance(x, y, poiSet):
	totalDistance = 0
	for poi in poiSet:
		totalDistance += abs(x - poi.x) + abs(y - poi.y)
	return totalDistance

########
# Main #
########
poiSet = getPointsOfInterestFromFile("input06")
grid = createGrid(poiSet)

# Part 1
poiSetNonInfinite = getPointsOfInterestWithNonInfiniteAreas(grid, poiSet)
(poi, areaSize) = findLargestNonInfiniteArea(grid, poiSetNonInfinite)
print("POI #{id} has the largest non-infinite area. Size is {size}".format(id=poi.id, size=areaSize))

# Part 2
areaSize = getSizeOfAreaWithTotalDistanceLessThan(grid, poiSet, 10000)
print("Size of region with total distance to all POIs < 10000: {}".format(areaSize))
