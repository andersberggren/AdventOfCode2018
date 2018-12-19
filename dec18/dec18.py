###########
# Classes #
###########
class World:
	def __init__(self, width, height, time=0):
		self.width = width
		self.height = height
		self.time = time
		self.trees = set()
		self.lumberyards = set()

	def addTree(self, position):
		self.trees.add(position)

	def addLumberyard(self, position):
		self.lumberyards.add(position)

	def getNextWorld(self):
		nextWorld = World(self.width, self.height, self.time+1)
		for y in range(self.height):
			for x in range(self.width):
				position = (x,y)
				(nTrees, nLumberyards) = self.getNumberOfAdjacentTreesAndLumberyards(position)
				if position in self.trees:
					if nLumberyards >= 3:
						nextWorld.addLumberyard(position)
					else:
						nextWorld.addTree(position)
				elif position in self.lumberyards:
					if nTrees >= 1 and nLumberyards >= 1:
						nextWorld.addLumberyard(position)
				else:
					if nTrees >= 3:
						nextWorld.addTree(position)
		return nextWorld

	# Returns (numberOfAdjacentTrees, numberOfAdjacentLumberyards)
	def getNumberOfAdjacentTreesAndLumberyards(self, position):
		xRange = range(position[0]-1, position[0]+2)
		yRange = range(position[1]-1, position[1]+2)
		positionsToCheck = [(x,y) for x in xRange for y in yRange if (x,y) != position]
		numberOfTrees = len([p for p in positionsToCheck if p in self.trees])
		numberOfLumberyards = len([p for p in positionsToCheck if p in self.lumberyards])
		return (numberOfTrees, numberOfLumberyards)

	def getResourceValue(self):
		return len(self.trees) * len(self.lumberyards)

	def toString(self):
		s = ""
		for y in range(self.height):
			for x in range(self.width):
				position = (x,y)
				if position in self.trees:
					s += "|"
				elif position in self.lumberyards:
					s += "#"
				else:
					s += "."
			s += "\n"
		return s

#############
# Functions #
#############
def readWorldFromFile(fileName):
	with open(fileName) as f:
		lines = f.readlines()
		width = len(lines[0].rstrip())
		height = len(lines)
		world = World(width, height)
		for y in range(len(lines)):
			line = lines[y].rstrip()
			for x in range(len(line)):
				position = (x,y)
				symbol = line[x]
				if symbol == "|":
					world.addTree(position)
				elif symbol == "#":
					world.addLumberyard(position)
	return world

def getResourceValueOfWorldAfterTime(initialWorld, targetTime):
	world = initialWorld
	stringToWorld = {}
	while world.time < targetTime:
		worldAsString = world.toString()
		if worldAsString in stringToWorld:
			timeAtBeginningOfLoop = stringToWorld[worldAsString].time
			loopSize = world.time - timeAtBeginningOfLoop
			equivalentFinalTime = timeAtBeginningOfLoop + ((targetTime-world.time) % loopSize)
			print("Pattern repeated at minute {a} and {b}".format(
					a=timeAtBeginningOfLoop, b=world.time))
			print("Resource value at minute {b} will be the same as at minute {a}".format(
					a=equivalentFinalTime, b=targetTime))
			finalWorld = next(w for w in stringToWorld.values() if w.time == equivalentFinalTime)
			return finalWorld.getResourceValue()
		stringToWorld[worldAsString] = world
		world = world.getNextWorld()
		print("Minute {m}, value {v}".format(m=world.time, v=world.getResourceValue()))
	return world.getResourceValue()

########
# Main #
########
if __name__ == "__main__":
	initialWorld = readWorldFromFile("input18")
	part1Answer = getResourceValueOfWorldAfterTime(initialWorld, 10)
	print("Part 1: {}".format(part1Answer))
	part2Answer = getResourceValueOfWorldAfterTime(initialWorld, 1000000000)
	print("Part 2: {}".format(part2Answer))
