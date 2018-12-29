import re

from aoclib.distance import getManhattanDistance3
from aoclib.sortedlist import SortedList

###########
# Classes #
###########
class Nanobot:
	def __init__(self, pos, radius):
		self.pos = pos
		self.radius = radius

class AStar:
	def __init__(self, initialNodes):
		self.nodeList = SortedList(ascending=False)
		for node in initialNodes:
			self.nodeList.insert(node)
		self.locationToTime = {}

	def findBestSolutions(self):
		nCreated = self.nodeList.getSize()
		nEvaluated = 0
		solutionNodes = []
		while not self.nodeList.isEmpty():
			node = self.nodeList.pop()
			nEvaluated += 1
			if len(solutionNodes) > 0 and node < solutionNodes[0]:
				break
			if node.isSolution():
				print("Found a solution!")
				solutionNodes.append(node)
			for successorNode in node.getSuccessorNodes():
				nCreated += 1
				self.nodeList.insert(successorNode)
				#if nCreated % 1000 == 0:
				#	print("Created: {c: >7}  In list: {l: >7}  Evaluated: {e: >7}".format(
				#			c=nCreated, l=self.nodeList.getSize(), e=nEvaluated))
		print("Created {c} nodes, evaluated {e} nodes".format(c=nCreated, e=nEvaluated))
		print("Number of solutions: {}".format(len(solutionNodes)))
		return solutionNodes

class SearchNode:
	def __init__(self, pos, size, nanobots):
		self.pos = pos
		self.size = size
		self.nanobots = nanobots
		self.nrNanobotsInRange = self.getNumberOfNanobotsInRange()
		#print("Bounding box: {} {} In range of {}".format(
		#		self.pos, self.size, self.nrNanobotsInRange))
	
	def getNumberOfNanobotsInRange(self):
		count = 0
		for nanobot in self.nanobots:
			if getManhattanDistanceFromBoxToPoint(self.pos, self.size, nanobot.pos) <= nanobot.radius:
				count += 1
		return count
	
	def getSuccessorNodes(self):
		if self.isSolution():
			return []
		successorNodes = []
		for x in range(2):
			if x == 0:
				xPos  = self.pos[0]
				xSize = self.size[0] // 2
			else:
				xPos  = self.pos[0]  + (self.size[0]//2)
				xSize = self.size[0] - (self.size[0]//2)
			for y in range(2):
				if y == 0:
					yPos  = self.pos[1]
					ySize = self.size[1] // 2
				else:
					yPos  = self.pos[1]  + (self.size[1]//2)
					ySize = self.size[1] - (self.size[1]//2)
				for z in range(2):
					if z == 0:
						zPos  = self.pos[2]
						zSize = self.size[2] // 2
					else:
						zPos  = self.pos[2]  + (self.size[2]//2)
						zSize = self.size[2] - (self.size[2]//2)
					newPos  = (xPos, yPos, zPos)
					newSize = (xSize, ySize, zSize)
					if all([s >= 1 for s in newSize]):
						newNode = SearchNode(newPos, newSize, nanobots)
						successorNodes.append(newNode)
		return successorNodes
	
	def isSolution(self):
		return all([x == 1 for x in self.size])

	def __le__(self, other):
		return self.nrNanobotsInRange <= other.nrNanobotsInRange
	
	def __lt__(self, other):
		return self.nrNanobotsInRange < other.nrNanobotsInRange

#############
# Functions #
#############
def getNanobotsFromFile(fileName):
	with open(fileName) as f:
		return [getNanobotFromString(x) for x in f.readlines()]

def getNanobotFromString(s):
	match = re.match("pos=<([0-9,-]+)>, r=(\d+)", s)
	pos = tuple([int(x) for x in match.group(1).split(",")])
	radius = int(match.group(2))
	return Nanobot(pos, radius)

def getManhattanDistanceFromBoxToPoint(boxPos, boxSize, pos):
	distance = 0
	for i in range(3):
		minValue = boxPos[i]
		maxValue = boxPos[i]+boxSize[i]-1
		distance += max(pos[i] - maxValue, minValue - pos[i], 0)
	return distance

# Returns (pos, size), where "pos" and "size" are 3-tuples.
def getBoundingBox(nanobots):
	minValues = list(nanobots[0].pos)
	maxValues = list(nanobots[0].pos)
	for nanobot in nanobots:
		for i in range(3):
			minValues[i] = min(minValues[i], nanobot.pos[i])
			maxValues[i] = max(maxValues[i], nanobot.pos[i])
	size = tuple([maxValues[i]-minValues[i]+1 for i in range(3)])
	return (tuple(minValues), size)

def part1(nanobots):
	strongestNanobot = sorted(nanobots, key=lambda x: x.radius, reverse=True)[0]
	part1 = len([x for x in nanobots
	             if getManhattanDistance3(x.pos, strongestNanobot.pos) <= strongestNanobot.radius])
	print("Part 1: {} nanobots are in range".format(part1))

def part2(nanobots):
	(pos, size) = getBoundingBox(nanobots)
	initialNode = SearchNode(pos, size, nanobots)
	aStar = AStar([initialNode])
	solutionNodes = aStar.findBestSolutions()
	for node in solutionNodes:
		print("Part 2: Distance is {}".format(getManhattanDistance3((0,0,0), node.pos)))

########
# Main #
########
if __name__ == "__main__":
	nanobots = getNanobotsFromFile("input23.txt")
	part1(nanobots)
	part2(nanobots)
