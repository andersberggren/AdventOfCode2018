import re

#########
# Class #
#########
class Point:
	# position  (x,y)-position
	# velocity  (x,y)-velocity
	def __init__(self, position, velocity):
		self.position = position
		self.velocity = velocity

	def update(self):
		self.position = (self.position[0]+self.velocity[0], self.position[1]+self.velocity[1])

	@staticmethod
	def createFromString(s):
		# String format example: position=<-42528,  42920> velocity=< 4, -4>
		match = re.match("position=< *(-?\d+), *(-?\d+)> velocity=< *(-?\d+), *(-?\d+)>", s)
		if match:
			position = (int(match.group(1)), int(match.group(2)))
			velocity = (int(match.group(3)), int(match.group(4)))
		else:
			raise ValueError("String has invalid format: {}".format(s))
		return Point(position, velocity)

#############
# Functions #
#############
def getPointListFromFile(fileName):
	with open(fileName) as f:
		return [Point.createFromString(line.strip()) for line in f.readlines()]

def getSpread(points):
	maxX = max([p.position[0] for p in points])
	minX = min([p.position[0] for p in points])
	maxY = max([p.position[1] for p in points])
	minY = min([p.position[1] for p in points])
	xSpread = abs(maxX-minX)
	ySpread = abs(maxY-minY)
	return (xSpread, ySpread)

def printPoints(points):
	points = set([p.position for p in points])
	maxX = max([p[0] for p in points])
	minX = min([p[0] for p in points])
	maxY = max([p[1] for p in points])
	minY = min([p[1] for p in points])
	print("Printing light...")
	for y in range(minY, maxY+1):
		for x in range(minX, maxX+1):
			if (x,y) in points:
				print("#", end="")
			else:
				print(".", end="")
		print("")

########
# Main #
########
points = getPointListFromFile("input10")
minSpread = None
currentSpread = None
while minSpread is None or currentSpread <= minSpread:
	[p.update() for p in points]
	(x, y) = getSpread(points)
	print("X spread: {x}, Y spread: {y}".format(x=x, y=y))
	currentSpread = y
	if minSpread is None or currentSpread < minSpread:
		minSpread = currentSpread
	if currentSpread < 20:
		printPoints(points)
