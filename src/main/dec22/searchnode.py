from aoclib.direction import Direction
from aoclib.geometry import getManhattanDistance2
from dec22.cave import Tool

class SearchNode:
	def __init__(self, parentNode, cave, location):
		self.parentNode = parentNode
		self.cave = cave
		self.location = location
		self.timeSpent = 0
		self.equippedTool = Tool.torch
		if self.parentNode is not None:
			self.timeSpent = self.parentNode.timeSpent + 1
			self.equippedTool = self.parentNode.equippedTool
		if self.equippedTool not in self.cave.getValidTools(self.location):
			self.equippedTool = self.cave.getCommonTool(self.location, self.parentNode.location)
			self.timeSpent += 7
		if self.location == self.cave.targetLocation and self.equippedTool != Tool.torch:
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
			newLocation = Direction.getNewLocation(self.location, direction)
			if (self.parentNode is not None and newLocation == self.parentNode.location) \
					or newLocation[0] < 0 or newLocation[1] < 0:
				continue
			successorNodes.append(SearchNode(self, self.cave, newLocation))
		return successorNodes
	
	def getState(self):
		return (self.location, self.equippedTool)
	
	def isSolution(self):
		return self.location == self.cave.targetLocation

	def __le__(self, other):
		return self.f < other.f or (self.f == other.f and self.g >= other.g)
	
	def __ne__(self, other):
		return self.f != other.f
	
	def __repr__(self):
		s = "SearchNode[location={l},timeSpent={time},equippedTool={tool}]"
		return s.format(l=self.location, time=self.timeSpent, tool=self.equippedTool.name)
