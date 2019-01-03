class World:
	creatureTypes = {"Elf", "Goblin"}
	symbolsCreature = {x[0] for x in creatureTypes}
	symbolOpen = "."
	symbolClosed = "#"
	
	def __init__(self):
		self.allPositions = set()
		self.positionToCreature = {}

	def addPosition(self, position):
		self.allPositions.add(position)

	def addCreature(self, creature):
		self.positionToCreature[creature.position] = creature

	def moveCreature(self, creature, newPosition):
		del self.positionToCreature[creature.position]
		creature.position = newPosition
		self.positionToCreature[creature.position] = creature

	def attackCreature(self, attacker, defender):
		defender.hitPoints -= attacker.attackPower
		if defender.hitPoints <= 0:
			del self.positionToCreature[defender.position]

	def getCreaturesSortedByExecutionOrder(self):
		return sorted(self.positionToCreature.values(), key=lambda x: positionSortKey(x.position))

	def getEnemies(self, friendType):
		return [x for x in self.positionToCreature.values() if x.type != friendType]

	def getAdjacentSquares(self, position):
		(x,y) = position
		positions = [(x,y+1), (x,y-1), (x+1,y), (x-1,y)]
		return set([p for p in positions if p in self.allPositions])

	def getAdjacentEmptySquares(self, position):
		return set([p for p in self.getAdjacentSquares(position) if self.isEmpty(p)])

	def getDistance(self, positionFrom, positionTo):
		visitedSquares = set([positionFrom])
		positionsAtThisDistance = set([positionFrom])
		distance = 0
		while len(positionsAtThisDistance) > 0:
			if positionTo in positionsAtThisDistance:
				return distance
			positionsAtNextDistance = set()
			for position in positionsAtThisDistance:
				for nextPosition in self.getAdjacentEmptySquares(position):
					if nextPosition not in visitedSquares:
						visitedSquares.add(position)
						positionsAtNextDistance.add(nextPosition)
			positionsAtThisDistance = positionsAtNextDistance
			distance += 1
		raise UnreachableError("No path from {f} to {t}".format(f=positionFrom, t=positionTo))

	def isCombatOver(self):
		# Combat is over if there is only one creature type left
		return len(set([creature.type for creature in self.positionToCreature.values()])) <= 1

	def isEmpty(self, position):
		return position in self.allPositions and position not in self.positionToCreature

	def isReachable(self, positionFrom, positionTo):
		evaluated = set()
		leftToEvaluate = set([positionFrom])
		while len(leftToEvaluate) > 0:
			position = leftToEvaluate.pop()
			if position == positionTo:
				return True
			evaluated.add(position)
			for adjacentPosition in self.getAdjacentEmptySquares(position):
				if adjacentPosition not in evaluated:
					leftToEvaluate.add(adjacentPosition)
		return False

	def existsAdjacentEnemy(self, creature):
		for position in self.getAdjacentSquares(creature.position):
			try:
				otherCreature = self.positionToCreature[position]
				if creature.type != otherCreature.type:
					return True
			except KeyError:
				# No creature at position. Ignore.
				pass
		return False
	
	def printWorld(self):
		maxX = max([pos[0] for pos in self.allPositions])
		maxY = max([pos[1] for pos in self.allPositions])
		for y in range(maxY+2):
			for x in range(maxX+2):
				position = (x,y)
				symbol = self.symbolClosed
				if position in self.positionToCreature:
					symbol = self.positionToCreature[position].type[0]
				elif position in self.allPositions:
					symbol = self.symbolOpen
				print(symbol, end="")
			print()
	
	@staticmethod
	def createFromString(s):
		world = World()
		lines = s.splitlines()
		for y in range(len(lines)):
			line = lines[y].strip()
			for x in range(len(line)):
				position = (x,y)
				symbol = line[x]
				creatureType = next((x for x in World.creatureTypes if x[0] == symbol), None)
				if symbol == World.symbolOpen:
					world.addPosition(position)
				elif creatureType is not None:
					world.addPosition(position)
					world.addCreature(Creature(position, creatureType))
		return world
		

class Creature:
	""" Represents a creature, such as an Elf or a Goblin """
	def __init__(self, position, creatureType):
		self.position = position
		self.type = creatureType
		self.attackPower = 3
		self.hitPoints = 200

class UnreachableError(Exception):
	pass

# Sort key for positions (x,y), to be sorted in reading order.
# Pass this function as "key" argument to sorted(listToSort, key=positionSortKey)
def positionSortKey(position):
	return (position[1], position[0])
