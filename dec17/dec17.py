import re

###########
# Classes #
###########
class World:
	def __init__(self):
		self.waterSpring = (500, 0)
		# Set of positions (x,y) with clay
		self.clay = set()
		# Set of positions (x,y) where water has settled
		self.waterSettled = set()
		# Set of positions (x,y) where water has passed, but not settled (yet)
		self.waterPassed = {self.waterSpring}
		self.minY = None
		self.maxY = None

	def addClay(self, topLeftX, topLeftY, width, height):
		for x in range(topLeftX, topLeftX+width):
			for y in range(topLeftY, topLeftY+height):
				self.clay.add((x,y))
		if self.minY is None:
			self.minY = topLeftY
		else:
			self.minY = min(self.minY, topLeftY)
		if self.maxY is None:
			self.maxY = topLeftY+height-1
		else:
			self.maxY = max(self.maxY, topLeftY+height-1)

	def letWaterFlow(self):
		i = 0
		while True:
			waterBefore = self.getWaterAmounts()
			for pos in [x for x in self.waterPassed if x[1] <= self.maxY]:
				self.letWaterFlowDown(pos)
				self.letWaterFlowSideways(pos)
				self.letWaterSettle(pos)
			self.waterPassed = self.waterPassed.difference(self.waterSettled)
			waterAfter = self.getWaterAmounts()
			i += 1
			print("Iteration {i}. Water amounts: {w}".format(i=i, w=waterAfter), flush=True)
			if waterBefore == waterAfter:
				return

	# Water spreads downwards.
	def letWaterFlowDown(self, pos):
		pos = getPositionBelow(pos)
		while self.isEmpty(pos) and pos[1] <= self.maxY:
			self.waterPassed.add(pos)
			pos = getPositionBelow(pos)

	# Water spreads sideways, if directly above clay or settled water.
	def letWaterFlowSideways(self, pos):
		if not self.hasSupportFromBelow(pos):
			return
		posLeft = pos
		while self.hasSupportFromBelow(posLeft):
			posLeft = getPositionLeft(posLeft)
			if self.isEmpty(posLeft):
				self.waterPassed.add(posLeft)
			else:
				break
		posRight = pos
		while self.hasSupportFromBelow(posRight):
			posRight = getPositionRight(posRight)
			if self.isEmpty(posRight):
				self.waterPassed.add(posRight)
			else:
				break

	# Water settles, if supported from left and right and below.
	def letWaterSettle(self, pos):
		supportRight = False
		supportLeft = False
		while not supportRight:
			if not self.hasSupportFromBelow(pos):
				return
			elif self.hasSupportFromRight(pos):
				supportRight = True
			else:
				pos = getPositionRight(pos)
		maxX = pos[0]
		while not supportLeft:
			if not self.hasSupportFromBelow(pos):
				return
			elif self.hasSupportFromLeft(pos):
				supportLeft = True
			else:
				pos = getPositionLeft(pos)
		minX = pos[0]
		for x in range(minX, maxX+1):
			self.waterSettled.add((x,pos[1]))

	def isEmpty(self, pos):
		return pos not in self.clay and pos not in self.waterSettled and pos not in self.waterPassed

	def canWaterSettle(self, pos):
		supportRight = False
		supportLeft = False
		while not supportRight:
			if not self.hasSupportFromBelow(pos):
				return False
			elif self.hasSupportFromRight(pos):
				supportRight = True
			else:
				pos = getPositionRight(pos)
		while not supportLeft:
			if not self.hasSupportFromBelow(pos):
				return False
			elif self.hasSupportFromLeft(pos):
				supportLeft = True
			else:
				pos = getPositionLeft(pos)
		return True

	def hasSupportFromBelow(self, pos):
		posBelow = getPositionBelow(pos)
		return posBelow in self.clay or posBelow in self.waterSettled

	def hasSupportFromLeft(self, pos):
		posLeft = getPositionLeft(pos)
		return posLeft in self.clay or posLeft in self.waterSettled

	def hasSupportFromRight(self, pos):
		posRight = getPositionRight(pos)
		return posRight in self.clay or posRight in self.waterSettled

	def getWaterAmounts(self):
		return (len(self.waterSettled), len(self.waterPassed))

#############
# Functions #
#############
def getWorldFromFile(fileName):
	world = World()
	with open(fileName) as f:
		for line in f.readlines():
			(x, y, width, height) = stringToRectangle(line)
			world.addClay(x, y, width, height)
	return world

# Reads a string and returns (x, y, width, height)
def stringToRectangle(s):
	xMatch = re.search("x=(\d+)(..(\d+))?", s)
	yMatch = re.search("y=(\d+)(..(\d+))?", s)
	x = int(xMatch.group(1))
	if xMatch.group(3) is None:
		width = 1
	else:
		width = int(xMatch.group(3)) + 1 - x
	y = int(yMatch.group(1))
	if yMatch.group(3) is None:
		height = 1
	else:
		height = int(yMatch.group(3)) + 1 - y
	return (x, y, width, height)

def getPositionBelow(pos):
	return (pos[0], pos[1]+1)

def getPositionLeft(pos):
	return (pos[0]-1, pos[1])

def getPositionRight(pos):
	return (pos[0]+1, pos[1])

def printWorld(world):
	minX = min([pos[0] for pos in world.clay])
	maxX = max([pos[0] for pos in world.clay])
	minY = min([pos[1] for pos in world.clay])
	maxY = max([pos[1] for pos in world.clay])
	for y in range(maxY+1):
		for x in range(minX, maxX+1):
			position = (x,y)
			symbol = " "
			if position in world.clay:
				symbol = "#"
			elif position == world.waterSpring:
				symbol = "+"
			elif position in world.waterSettled:
				symbol = "~"
			elif position in world.waterPassed:
				symbol = "|"
			print(symbol, end="")
		print()

########
# Main #
########
world = getWorldFromFile("input17")
world.letWaterFlow()
printWorld(world)
allWaterPositions = world.waterSettled | world.waterPassed
part1Answer = len([1 for (x,y) in allWaterPositions if y >= world.minY and y <= world.maxY])
print("Part 1. Number of squares with water: {}".format(part1Answer))
part2Answer = len([1 for (x,y) in world.waterSettled if y >= world.minY and y <= world.maxY])
print("Part 2. Number of squares with settled water: {}".format(part2Answer))
