import re

from aoclib.geometry import getBoundingBox
from aoclib.geometry import getManhattanDistance3
from aoclib.geometry import getManhattanDistance3FromBox
from aoclib.geometry import getSubBoxes
from aoclib.filereader import getFileAsListOfString
from aoclib.search import AStar
from aoclib.sortedlist import SortedList

###########
# Classes #
###########
class Nanobot:
	def __init__(self, pos, radius):
		self.pos = pos
		self.radius = radius
	
	@staticmethod
	def createFromString(s):
		match = re.match("pos=<([0-9,-]+)>, r=(\d+)", s)
		pos = tuple([int(x) for x in match.group(1).split(",")])
		radius = int(match.group(2))
		return Nanobot(pos, radius)

class SearchNode:
	def __init__(self, pos, size, nanobots):
		self.pos = pos
		self.size = size
		self.nanobots = nanobots
		self.nrNanobotsInRange = len([x for x in self.nanobots if self.isInRange(x)])
	
	def getState(self):
		return (self.pos, self.size)
	
	def getSuccessorNodes(self):
		"""
		Creates 8 successor nodes, by splitting this nodes volume in half along all 3 dimensions.
		"""
		if self.isSolution():
			return []
		return [SearchNode(pos, size, nanobots) for (pos, size) in getSubBoxes(self.pos, self.size)]
	
	def isSolution(self):
		return all(x == 1 for x in self.size)
	
	def isInRange(self, nanobot):
		return getManhattanDistance3FromBox(self.pos, self.size, nanobot.pos) <= nanobot.radius
	
	def __le__(self, other):
		return self.nrNanobotsInRange <= other.nrNanobotsInRange
	
	def __ne__(self, other):
		return self.nrNanobotsInRange != other.nrNanobotsInRange

#############
# Functions #
#############
def part1(nanobots):
	strongestNanobot = sorted(nanobots, key=lambda x: x.radius, reverse=True)[0]
	part1 = len([x for x in nanobots
	             if getManhattanDistance3(x.pos, strongestNanobot.pos) <= strongestNanobot.radius])
	print("Part 1: {} nanobots are in range".format(part1))

def part2(nanobots):
	(pos, size) = getBoundingBox([x.pos for x in nanobots])
	initialNode = SearchNode(pos, size, nanobots)
	(solutionNodes, stats) = AStar([initialNode], ascending=False).findBestSolutions()
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
	nanobots = [Nanobot.createFromString(x) for x in getFileAsListOfString("input23.txt")]
	part1(nanobots)
	part2(nanobots)
