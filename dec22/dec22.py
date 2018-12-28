import re
import sys

###########
# Classes #
###########
class AStar:
	def __init__(self, initialNode):
		self.nodeList = [initialNode]
		self.locationToToolAndTime = {}

	def findBestSolution(self):
		while self.nodeList:
			node = self.nodeList.pop(0)
			if self.canSkip(node):
				print("Skip this node. We've already evaluated one that's at least as good.")
				continue
			if node.isSolution():
				print("Found solution!")
				return node
			self.nodeList.extend(node.getSuccessorNodes())
			self.nodeList = sorted(self.nodeList, key=lambda x: x.f())
		print("All nodes evaluated. No solution found.")
	
	def canSkip(self, node):
		try:
			(tool, timeSpent) = self.locationToToolAndTime[node.location]
			if node.equippedTool == tool:
				if node.timeSpent < timeSpent:
					self.locationToToolAndTime[node.location] = (node.equippedTool, node.timeSpent)
					return False
				else:
					return True
			else:
				# Different tool equipped
				if node.timeSpent < timeSpent:
					self.locationToToolAndTime[node.location] = (node.equippedTool, node.timeSpent)
					return False
				else:
					return node.timeSpent >= timeSpent+7
		except KeyError:
			self.locationToToolAndTime[node.location] = (node.equippedTool, node.timeSpent)
			return False

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
		print("Node at {l}, tool {tool}, time {time}".format(
				l=self.location, tool=self.equippedTool, time=self.timeSpent))
	
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

	# Returns the sum of cost so far and heuristic cost to solution.
	def f(self):
		return self.timeSpent + getManhattanDistance(self.location, self.cave.targetLocation)

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
	def __init__(self, name, risk, validTools):
		self.name = name
		self.risk = risk
		self.validTools = validTools
	
	@staticmethod
	def getRegionType(erosionLevel):
		return RegionType.all[erosionLevel % 3]

RegionType.rocky  = RegionType("Rocky",  0, {Tool.torch, Tool.climbingGear})
RegionType.wet    = RegionType("Wet",    1, {Tool.empty, Tool.climbingGear})
RegionType.narrow = RegionType("Narrow", 2, {Tool.empty, Tool.torch})
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

def getManhattanDistance(coordinateA, coordinateB):
	return abs(coordinateA[0] - coordinateB[0]) + abs(coordinateA[1] - coordinateB[1])

def getLocation(location, direction):
	return (location[0]+direction[0], location[1]+direction[1])

########
# Main #
########
(depth, targetLocation) = getDepthAndTargetLocationFromFile("input22.txt")
cave = Cave(depth, targetLocation)
cave.createRegion((cave.targetLocation[0], cave.targetLocation[1]+1))
print("Total risk: {}".format(cave.getTotalRisk()))

initialNode = SearchNode(None, cave, (0,0))
aStar = AStar(initialNode)
solutionNode = aStar.findBestSolution()
