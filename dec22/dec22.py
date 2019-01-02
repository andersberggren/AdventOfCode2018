import re
import sys

from aoclib.geometry import getManhattanDistance2
from aoclib.sortedlist import SortedList

###########
# Classes #
###########
class AStar:
	def __init__(self, initialNodes):
		self.nodeList = SortedList()
		for node in initialNodes:
			self.nodeList.insert(node)
		self.locationToTime = {}

	def findBestSolution(self):
		nCreated = 1
		nEvaluated = 0
		nSkipped = 0
		while not self.nodeList.isEmpty():
			node = self.nodeList.pop()
			if self.canSkip(node):
				nSkipped += 1
				continue
			else:
				nEvaluated += 1
				self.updateToolAndTime(node)
			if node.isSolution():
				print("Found solution!")
				return node
			for successorNode in node.getSuccessorNodes():
				nCreated += 1
				if self.canSkip(successorNode):
					nSkipped += 1
				else:
					self.nodeList.insert(successorNode)
				if nCreated % 10000 == 0:
					print("Created: {c: >7}  In list: {l: >7}  Evaluated: {e: >7}  Skipped: {s: >7}".format(
							c=nCreated, l=self.nodeList.getSize(), e=nEvaluated, s=nSkipped))
					print("Current node is at {l} after {t} minutes. f() = {f}".format(
						l=node.location, t=node.timeSpent, f=node.f))
		print("All nodes evaluated. No solution found.")
	
	def canSkip(self, node):
		key = (node.location[0], node.location[1], node.equippedTool)
		try:
			return node.timeSpent >= self.locationToTime[key]
		except KeyError:
			return False
	
	def updateToolAndTime(self, node):
		key = (node.location[0], node.location[1], node.equippedTool)
		try:
			timeSpent = self.locationToTime[key]
			if node.timeSpent < timeSpent:
				self.locationToTime[key] = node.timeSpent
		except KeyError:
			self.locationToTime[key] = node.timeSpent

class SearchNode:
	def __init__(self, parentNode, cave, location):
		self.parentNode = parentNode
		self.cave = cave
		self.location = location
		self.previousLocations = {self.location}
		self.timeSpent = 0
		self.equippedTool = Tool.torch
		if self.parentNode is not None:
			self.previousLocations |= self.parentNode.previousLocations
			self.timeSpent = self.parentNode.timeSpent + 1
			self.equippedTool = self.parentNode.equippedTool
		if self.equippedTool not in self.cave.getValidTools(self.location):
			self.equippedTool = self.cave.getCommonTool(self.location, self.parentNode.location)
			self.timeSpent += 7
		elif self.location == self.cave.targetLocation and self.equippedTool != Tool.torch:
			self.equippedTool = Tool.torch
			self.timeSpent += 7
		# g: Cost so far
		# h: Heuristic estimate of remaining cost to solution (must not overestimate)
		# f: g + h
		self.g = self.timeSpent
		self.h = getManhattanDistance2(self.location, self.cave.targetLocation)
		self.f = self.g + self.h
	
	def getSuccessorNodes(self):
		successorNodes = []
		for direction in Direction.all:
			newLocation = getLocation(self.location, direction)
			if (self.parentNode is not None and newLocation == self.parentNode.location) \
					or newLocation[0] < 0 or newLocation[1] < 0 \
					or newLocation in self.previousLocations:
				continue
			successorNodes.append(SearchNode(self, self.cave, newLocation))
		return successorNodes
	
	def isSolution(self):
		return self.location == self.cave.targetLocation

	def __le__(self, other):
		return self.f < other.f or (self.f == other.f and self.g >= other.g)

class Direction:
	up    = ( 0, -1)
	down  = ( 0,  1)
	left  = (-1,  0)
	right = ( 1,  0)
	all = [up, down, left, right]

class Cave:
	def __init__(self, depth, targetLocation):
		self.depth = depth
		self.targetLocation = targetLocation
		self.locationToRegion = {}
		self.createRegions()

	def createRegions(self):
		for x in range(self.targetLocation[0]+1):
			for y in range(self.targetLocation[1]+1):
				self.createRegion((x,y))

	def createRegion(self, location):
		region = Region(location)
		self.locationToRegion[location] = region
		region.geologicIndex = self.getGeologicIndex(location)
		region.erosionLevel = (region.geologicIndex+self.depth) % 20183
		region.type = RegionType.getRegionType(region.erosionLevel)
		return region

	# Returns the Region at "location". Creates the Region if it doesn't already exist.
	def getRegion(self, location):
		try:
			return self.locationToRegion[location]
		except KeyError:
			return self.createRegion(location)
	
	def getGeologicIndex(self, location):
		(x,y) = location
		if location == (0,0):
			return 0
		elif location == self.targetLocation:
			return 0
		elif y == 0:
			return x * 16807
		elif x == 0:
			return y * 48271
		else:
			return self.getErosionLevel((x-1,y)) * self.getErosionLevel((x,y-1))

	def getErosionLevel(self, location):
		return self.getRegion(location).erosionLevel

	def getRisk(self, location):
		return self.getRegion(location).type.risk
	
	def getTotalRisk(self):
		xRange = range(self.targetLocation[0]+1)
		yRange = range(self.targetLocation[1]+1)
		return sum([cave.locationToRegion[(x,y)].type.risk for x in xRange for y in yRange])

	def getValidTools(self, location):
		return self.getRegion(location).type.validTools
	
	def getCommonTool(self, locationA, locationB):
		commonTools = self.getRegion(locationA).type.validTools & self.getRegion(locationB).type.validTools
		if len(commonTools) != 1:
			print("Location {a} and {b} have {n} tools in common. Expected 1.". format(
					a=locationA, b=locationB, n=len(commonTools)))
			sys.exit(1)
		return commonTools.pop()
	
	def printCave(self):
		for y in range(self.targetLocation[1]+6):
			for x in range(self.targetLocation[0]+6):
				location = (x,y)
				symbol = self.getRegion(location).type.symbol
				if location == (0,0):
					symbol = "M"
				elif location == self.targetLocation:
					symbol = "T"
				print(symbol, end="")
			print()

class Tool:
	def __init__(self, name):
		self.name = name

Tool.empty = Tool("Empty")
Tool.torch = Tool("Torch")
Tool.climbingGear = Tool("Climbing gear")

class Region:
	def __init__(self, location):
		self.location = location
		self.geologicIndex = None
		self.erosionLevel = None
		self.type = None

class RegionType:
	def __init__(self, symbol, risk, validTools):
		self.symbol = symbol
		self.risk = risk
		self.validTools = validTools
	
	@staticmethod
	def getRegionType(erosionLevel):
		return RegionType.all[erosionLevel % 3]

RegionType.rocky  = RegionType(".", 0, {Tool.torch, Tool.climbingGear})
RegionType.wet    = RegionType("=", 1, {Tool.empty, Tool.climbingGear})
RegionType.narrow = RegionType("|", 2, {Tool.empty, Tool.torch})
RegionType.all = [RegionType.rocky, RegionType.wet, RegionType.narrow]

#############
# Functions #
#############
# Returns (depth, targetLocation)
def getDepthAndTargetLocationFromFile(fileName):
	with open(fileName) as f:
		for line in f.readlines():
			depthMatch = re.match("^depth: (\d+)$", line)
			targetMatch = re.match("^target: (\d+),(\d+)", line)
			if depthMatch:
				depth = int(depthMatch.group(1))
			elif targetMatch:
				target = (int(targetMatch.group(1)), int(targetMatch.group(2)))
	return (depth, target)

def getLocation(location, direction):
	return (location[0]+direction[0], location[1]+direction[1])

########
# Main #
########
(depth, targetLocation) = getDepthAndTargetLocationFromFile("input22.txt")
#depth = 510
#targetLocation = (10,10)
cave = Cave(depth, targetLocation)
#cave.printCave()
print("Total risk: {}".format(cave.getTotalRisk()))

# Part 2
initialNode = SearchNode(None, cave, (0,0))
aStar = AStar([initialNode])
solutionNode = aStar.findBestSolution()
print("Solution found. Time to reach target: {}".format(solutionNode.timeSpent))
