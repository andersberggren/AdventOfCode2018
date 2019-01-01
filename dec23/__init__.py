import re

from aoclib.distance import getManhattanDistance3
from aoclib.distance import getManhattanDistance3FromCuboid
from aoclib.search import AStar
from aoclib.sortedlist import SortedList

###########
# Classes #
###########
class Nanobot:
	def __init__(self, pos, radius):
		self.pos = pos
		self.radius = radius

class SearchNode:
	def __init__(self, pos, size, nanobots):
		self.pos = pos
		self.size = size
		self.nanobots = nanobots
		self.nrNanobotsInRange = 0
		for nanobot in self.nanobots:
			if getManhattanDistance3FromCuboid(self.pos, self.size, nanobot.pos) <= nanobot.radius:
				self.nrNanobotsInRange += 1
	
	def getState(self):
		return (self.pos, self.size)
	
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
	
	def __ne__(self, other):
		return self.nrNanobotsInRange != other.nrNanobotsInRange
	
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
	aStar = AStar([initialNode], ascending=False)
	(solutionNodes, stats) = aStar.findBestSolutions()
	print("Nodes created: {c}  Evaluated: {e}  Skipped: {s}  Remaining in list: {l}".format(
			c=stats.created, e=stats.evaluated, s=stats.skipped,
			l=stats.created-(stats.evaluated+stats.skipped)))
	print("Number of solutions: {}".format(len(solutionNodes)))
	for node in solutionNodes:
		print("Part 2: Distance is {}".format(getManhattanDistance3((0,0,0), node.pos)))

########
# Main #
########
if __name__ == "__main__":
	nanobots = getNanobotsFromFile("input23.txt")
	part1(nanobots)
	part2(nanobots)
