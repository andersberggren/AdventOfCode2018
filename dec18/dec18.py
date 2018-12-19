import sys

###########
# Classes #
###########
class World:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.trees = set()
		self.lumberyards = set()

	def addTree(self, position):
		self.trees.add(position)

	def addLumberyard(self, position):
		self.lumberyards.add(position)

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
		for y in range(world.height):
			for x in range(world.width):
				position = (x,y)
				symbol = "."
				if position in world.trees:
					symbol = "|"
				elif position in world.lumberyards:
					symbol = "#"
				s += symbol
			s += "\n"
		return s

#############
# Functions #
#############
def readWorldFromFile(fileName):
	world = World(50, 50)
	with open(fileName) as f:
		lines = f.readlines()
		for y in range(len(lines)):
			line = lines[y].rstrip()
			for x in range(len(line)):
				position = (x,y)
				symbol = line[x]
				if symbol == "|":
					world.addTree(position)
				elif symbol == "#":
					world.addLumberyard(position)
				elif symbol == ".":
					pass
				else:
					print("Invalid symbol at {pos}: {s}".format(pos=position, s=symbol))
					sys.exit(1)
	return world

def getNextWorld(world):
	nextWorld = World(world.width, world.height)
	for y in range(world.height):
		for x in range(world.width):
			position = (x,y)
			(nTrees, nLumberyards) = world.getNumberOfAdjacentTreesAndLumberyards(position)
			#print("Position {p} has {t} trees and {l} lumberyards".format(
			#		p=position, t=nTrees, l=nLumberyards))
			if position in world.trees:
				if nLumberyards >= 3:
					nextWorld.addLumberyard(position)
				else:
					nextWorld.addTree(position)
			elif position in world.lumberyards:
				if nTrees >= 1 and nLumberyards >= 1:
					nextWorld.addLumberyard(position)
			else:
				if nTrees >= 3:
					nextWorld.addTree(position)
	return nextWorld

########
# Main #
########
# Part 1
world = readWorldFromFile("input18")
for i in range(10):
	world = getNextWorld(world)
numberOfTrees = len(world.trees)
numberOfLumberyards = len(world.lumberyards)
print("Part 1: {}".format(numberOfTrees*numberOfLumberyards))

# Part 2
world = readWorldFromFile("input18")
worldToTimeAndValue = {}
targetTime = 1000000000
for i in range(targetTime):
	worldAsString = world.toString()
	if worldAsString in worldToTimeAndValue:
		print("Pattern repeated after {} minutes".format(i))
		timeAtBeginningOfLoop = worldToTimeAndValue[worldAsString][0]
		loopSize = i - timeAtBeginningOfLoop
		timeLeft = (targetTime-i) % loopSize
		finalTime = timeAtBeginningOfLoop + timeLeft
		for (time, value) in worldToTimeAndValue.values():
			if time == finalTime:
				print("Part 2: {}".format(value))
				sys.exit(0)
		print("Couldn't find final value")
		sys.exit(1)
	else:
		worldToTimeAndValue[worldAsString] = (i, world.getResourceValue())
	world = getNextWorld(world)
