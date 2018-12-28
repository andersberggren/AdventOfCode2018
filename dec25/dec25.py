from aoclib.distance import getManhattanDistance4

###########
# Classes #
###########
class Constellation:
	def __init__(self):
		self.members = set()

	def addPoint(self, point):
		self.members.add(point)

#############
# Functions #
#############
def getPointsFromFile(fileName):
	with open(fileName) as f:
		return set([getPointFromString(x) for x in f.readlines()])

def getPointFromString(s):
	return tuple([int(x) for x in s.strip().split(",")])

def joinConstellations(constellationA, constellationB, pointToConstellation):
	for point in constellationB.members:
		constellationA.addPoint(point)
		pointToConstellation[point] = constellationA

########
# Main #
########
points = getPointsFromFile("input25.txt")
pointToConstellation = {}
for point in points:
	constellation = Constellation()
	constellation.addPoint(point)
	pointToConstellation[point] = constellation

progress = True
while progress:
	progress = False
	for pointA in set(points):
		constellationA = pointToConstellation[pointA]
		for pointB in set(points):
			constellationB = pointToConstellation[pointB]
			if constellationA != constellationB and getManhattanDistance4(pointA, pointB) <= 3:
				joinConstellations(constellationA, constellationB, pointToConstellation)
				progress = True
				numberOfConstellations = len(set(pointToConstellation.values()))
				print("Joined two constellations. Remaining constellations: {}".format(numberOfConstellations))
numberOfConstellations = len(set(pointToConstellation.values()))
print("No more joins can be done. Remaining constellations: {}".format(numberOfConstellations))
