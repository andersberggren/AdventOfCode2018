import re

#########
# Class #
#########
class Light:
	# position  Tuple with (x,y)-position
	# velocity  Tuple with (x,y)-velocity
	def __init__(self, position, velocity):
		self.position = position
		self.velocity = velocity

	def update(self):
		self.position = (self.position[0]+self.velocity[0], self.position[1]+self.velocity[1])

#############
# Functions #
#############
def getLightListFromFile(fileName):
	with open(fileName) as f:
		return [createLightFromString(line.strip()) for line in f.readlines()]

def createLightFromString(s):
	# String format example: position=<-42528,  42920> velocity=< 4, -4>
	match = re.match("position=< *(-?\d+), *(-?\d+)> velocity=< *(-?\d+), *(-?\d+)>", s)
	if match:
		position = (int(match.group(1)), int(match.group(2)))
		velocity = (int(match.group(3)), int(match.group(4)))
	else:
		raise ValueError("String has invalid format: {}".format(s))
	return Light(position, velocity)

# Returns number of seconds required for the lights to group together.
def updateUntilLightsAreGroupedTogether(lights):
	time = 0
	while not areGroupedTogether(lights):
		for light in lights:
			light.update()
		time += 1
	return time

def areGroupedTogether(lights):
	positions = set([light.position for light in lights])
	for position in positions:
		if not hasNeighbor(position, positions):
			return False
	return True

def hasNeighbor(position, positions):
	x = position[0]
	y = position[1]
	for xIter in range(x-1, x+2):
		for yIter in range(y-1, y+2):
			if not (xIter == x and yIter == y) and (xIter,yIter) in positions:
				return True
	return False

def printLights(lights):
	positions = set([light.position for light in lights])
	minX = min([p[0] for p in positions])
	maxX = max([p[0] for p in positions])
	minY = min([p[1] for p in positions])
	maxY = max([p[1] for p in positions])
	for y in range(minY, maxY+1):
		for x in range(minX, maxX+1):
			if (x,y) in positions:
				print("#", end="")
			else:
				print(" ", end="")
		print("")

########
# Main #
########
lights = getLightListFromFile("input10.txt")
time = updateUntilLightsAreGroupedTogether(lights)
print("After {} seconds, the lights are grouped together. Message:".format(time))
printLights(lights)
