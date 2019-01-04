class World:
	def __init__(self):
		self.waterSpring = (500, 0)
		# Set of positions (x,y) with clay
		self.clay = set()
		# Set of positions (x,y) where water has passed
		self.waterPassed = {self.waterSpring}
		# Set of positions (x,y) where water has settled
		self.waterSettled = set()
		self.minY = None
		self.maxY = None

	def addClay(self, topLeftX, topLeftY, width, height):
		for x in range(topLeftX, topLeftX+width):
			for y in range(topLeftY, topLeftY+height):
				self.clay.add((x,y))
		self.minY = topLeftY if self.minY is None else min(self.minY, topLeftY)
		self.maxY = topLeftY+height-1 if self.maxY is None else max(self.maxY, topLeftY+height-1)

	def letWaterFlow(self):
		newPositionsToEvaluate = {self.waterSpring}
		while newPositionsToEvaluate:
			positionsToEvaluateThisIteration = newPositionsToEvaluate
			newPositionsToEvaluate = set()
			for pos in positionsToEvaluateThisIteration:
				newPositionsToEvaluate |= self.letWaterFlowDown(pos)
				newPositionsToEvaluate |= self.letWaterFlowSideways(pos)
				newPositionsToEvaluate |= self.letWaterSettle(pos)

	def letWaterFlowDown(self, pos):
		"""
		Water spreads downwards.
		Returns a set of positions that needs to be evaluated during next iteration.
		"""
		newPositionsToEvaluate = set()
		while True:
			pos = getPositionBelow(pos)
			if not (pos[1] <= self.maxY and self.isEmpty(pos)):
				break
			self.waterPassed.add(pos)
			newPositionsToEvaluate.add(pos)
		return newPositionsToEvaluate

	def letWaterFlowSideways(self, pos):
		"""
		Water spreads sideways, if directly above clay or settled water.
		Returns a set of positions that needs to be evaluated during next iteration.
		"""
		newPositionsToEvaluate = set()
		if not self.hasSupportFromBelow(pos):
			return set()
		posLeft = pos
		while self.hasSupportFromBelow(posLeft):
			posLeft = getPositionLeft(posLeft)
			if self.isEmpty(posLeft):
				self.waterPassed.add(posLeft)
				newPositionsToEvaluate.add(posLeft)
			else:
				break
		posRight = pos
		while self.hasSupportFromBelow(posRight):
			posRight = getPositionRight(posRight)
			if self.isEmpty(posRight):
				self.waterPassed.add(posRight)
				newPositionsToEvaluate.add(posRight)
			else:
				break
		return newPositionsToEvaluate

	def letWaterSettle(self, pos):
		"""
		Water settles, if supported from left and right and below.
		Returns a set of positions that needs to be evaluated during next iteration.
		"""
		supportRight = False
		supportLeft = False
		while not supportRight:
			if not self.hasSupportFromBelow(pos):
				return set()
			elif self.hasSupportFromRight(pos):
				supportRight = True
			else:
				pos = getPositionRight(pos)
		maxX = pos[0]
		while not supportLeft:
			if not self.hasSupportFromBelow(pos):
				return set()
			elif self.hasSupportFromLeft(pos):
				supportLeft = True
			else:
				pos = getPositionLeft(pos)
		minX = pos[0]
		newPositionsToEvaluate = set()
		for x in range(minX, maxX+1):
			positionToSettle = (x,pos[1])
			if positionToSettle not in self.waterSettled:
				self.waterPassed.add(positionToSettle)
				self.waterSettled.add(positionToSettle)
				posAbove = getPositionAbove(positionToSettle)
				if posAbove in self.waterPassed:
					newPositionsToEvaluate.add(posAbove)
		return newPositionsToEvaluate

	def getWaterAmounts(self):
		return (len(self.waterSettled), len(self.waterPassed))

	def isEmpty(self, pos):
		return pos not in self.clay and pos not in self.waterSettled and pos not in self.waterPassed

	def hasSupportFromBelow(self, pos):
		posBelow = getPositionBelow(pos)
		return posBelow in self.clay or posBelow in self.waterSettled

	def hasSupportFromLeft(self, pos):
		posLeft = getPositionLeft(pos)
		return posLeft in self.clay or posLeft in self.waterSettled

	def hasSupportFromRight(self, pos):
		posRight = getPositionRight(pos)
		return posRight in self.clay or posRight in self.waterSettled

def getPositionAbove(pos):
	return (pos[0], pos[1]-1)

def getPositionBelow(pos):
	return (pos[0], pos[1]+1)

def getPositionLeft(pos):
	return (pos[0]-1, pos[1])

def getPositionRight(pos):
	return (pos[0]+1, pos[1])
