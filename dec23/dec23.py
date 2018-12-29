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
		nCreated = len(self.nodeList)
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
				if nCreated % 1000 == 0:
					print("Created: {c: >7}  In list: {l: >7}  Evaluated: {e: >7}".format(
							c=nCreated, l=self.nodeList.getSize(), e=nEvaluated))
		print("Number of solutions: {}".format(len(solutionNodes)))
		return solutionNodes

class SearchNode:
	def __init__(self, pos, size, nanobots):
		self.pos = pos
		self.size = size
		self.nanobots = nanobots
		self.nrNanobotsInRange = self.getNumberOfNanobotsInRange()
	
	def getNumberOfNanobotsInRange(self):
		# TODO Implement
		return 0
	
	def getSuccessorNodes(self):
		successorNodes = []
		# TODO Implement
		# Divide pos/size in 8 "quadrants"
		return successorNodes
	
	def isSolution(self):
		return all([x == 1 for x in self.size])

	def __le__(self, other):
		return self.nrNanobotsInRange <= other.nrNanobotsInRange

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

def getManhattanDistanceFromAreaToPoint(areaPos, areaSize, pos):
	# TODO Implement
	pass

########
# Main #
########
nanobots = getNanobotsFromFile("input23.txt")
strongestNanobot = sorted(nanobots, key=lambda x: x.radius, reverse=True)[0]
part1 = len([x for x in nanobots if getManhattanDistance3(x.pos, strongestNanobot.pos) <= strongestNanobot.radius])
print("Part 1: {} nanobots are in range".format(part1))
