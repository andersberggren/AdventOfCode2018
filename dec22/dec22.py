import re

###########
# Classes #
###########
class Cave:
	def __init__(self, depth, targetLocation):
		self.depth = depth
		self.targetLocation = targetLocation
		self.locationToRegion = {}
		self.createRegions()

	def createRegions(self):
		for x in range(self.targetLocation[0]+1):
			for y in range(self.targetLocation[1]+1):
				location = (x,y)
				region = Region(location)
				self.locationToRegion[location] = region
				region.geologicIndex = self.getGeologicIndex(region)
				region.erosionLevel = (region.geologicIndex+self.depth) % 20183
				region.risk = region.erosionLevel % 3

	def getGeologicIndex(self, region):
		(x,y) = region.location
		if (x,y) == (0,0):
			return 0
		elif (x,y) == self.targetLocation:
			return 0
		elif y == 0:
			return x * 16807
		elif x == 0:
			return y * 48271
		else:
			neighborA = self.locationToRegion[(x-1,y)]
			neighborB = self.locationToRegion[(x,y-1)]
			return neighborA.erosionLevel * neighborB.erosionLevel

	def getTotalRisk(self):
		xRange = range(self.targetLocation[0]+1)
		yRange = range(self.targetLocation[1]+1)
		return sum([cave.locationToRegion[(x,y)].risk for x in xRange for y in yRange])

class Region:
	def __init__(self, location):
		self.location = location
		self.geologicIndex = None
		self.erosionLevel = None
		self.risk = None

#############
# Functions #
#############
# Returns (depth, targetLocation)
def getDepthAndTargetLocationFromFile(fileName):
	with open(fileName) as f:
		for line in f.readlines():
			depthMatch = re.match("^depth: (\d+)$", line)
			targetMatch = re.match("^target: (\d+),(\d+)", line)
			if depthMatch:
				depth = int(depthMatch.group(1))
			elif targetMatch:
				target = (int(targetMatch.group(1)), int(targetMatch.group(2)))
	return (depth, target)

########
# Main #
########
(depth, targetLocation) = getDepthAndTargetLocationFromFile("input22.txt")
cave = Cave(depth, targetLocation)
print("Total risk: {}".format(cave.getTotalRisk()))
