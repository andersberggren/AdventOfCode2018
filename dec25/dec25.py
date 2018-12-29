from aoclib.distance import getManhattanDistance4
from aoclib.filereader import getFileAsListOfString

###########
# Classes #
###########
class Constellation:
	def __init__(self, point):
		self.members = {point}

	def addPoint(self, point):
		self.members.add(point)

#############
# Functions #
#############
def getPointsFromFile(fileName):
	return set([getPointFromString(x) for x in getFileAsListOfString(fileName)])

def getPointFromString(s):
	return tuple([int(x) for x in s.strip().split(",")])

def tryToJoinConstellations(pointToConstellation):
	progress = True
	while progress:
		progress = False
		points = list(pointToConstellation.keys())
		for i in range(len(points)):
			pointA = points[i]
			constellationA = pointToConstellation[pointA]
			for pointB in points[i+1:]:
				constellationB = pointToConstellation[pointB]
				if constellationA != constellationB and getManhattanDistance4(pointA, pointB) <= 3:
					joinConstellations(constellationA, constellationB, pointToConstellation)
					progress = True
	print("Part 1: Number of constellations: {}".format(len(set(pointToConstellation.values()))))

def joinConstellations(constellationA, constellationB, pointToConstellation):
	for point in constellationB.members:
		constellationA.addPoint(point)
		pointToConstellation[point] = constellationA
	constellationB.members = []

########
# Main #
########
if __name__ == "__main__":
	pointToConstellation = {p: Constellation(p) for p in getPointsFromFile("input25.txt")}
	tryToJoinConstellations(pointToConstellation)
