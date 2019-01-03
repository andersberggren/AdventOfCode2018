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

	def getAdjacentEnemy(self, creature):
		adjacentSquares = self.getAdjacentSquares(creature.position)
		# Get adjacent enemies, sorted by hit points
		adjacentEnemies = sorted(
			[x for x in self.getEnemies(creature.type) if x.position in adjacentSquares],
			key=lambda x: x.hitPoints
		)
		if not adjacentEnemies:
			return None
		# If there are multiple adjacent enemies with lowest hit points,
		# select the enemy which is first in reading order.
		return sorted(
			[x for x in adjacentEnemies if x.hitPoints == adjacentEnemies[0].hitPoints],
			key=lambda x: positionSortKey(x.position)
		)[0]

	def getAdjacentSquares(self, position):
		(x,y) = position
		positions = [(x,y+1), (x,y-1), (x+1,y), (x-1,y)]
		return {p for p in positions if p in self.allPositions}

	def getAdjacentEmptySquares(self, position):
		return {p for p in self.getAdjacentSquares(position) if self.isEmpty(p)}

	def getClosestReachableSquare(self, positionFrom, targetSquares):
		"""
		Returns the closest of the squares in targetSqures that is reachable from positionFrom,
		or None if none of the squares are reachable.
		Arguments:
		  positionFrom   Position (x,y)
		  targetSquares  A set of positions (x,y)
		"""
		visitedSquares = {positionFrom}
		fringe = {positionFrom}
		while len(fringe) > 0:
			reachableTargetSquares = fringe & targetSquares
			if len(reachableTargetSquares) > 0:
				return sorted(reachableTargetSquares, key=positionSortKey)[0]
			visitedSquares |= fringe
			fringe = {adj for f in fringe for adj in self.getAdjacentEmptySquares(f)
			          if adj not in visitedSquares
			}
		return None
	
	def isCombatOver(self):
		""" Combat is over if there is only one creature type left. """
		return len(set([creature.type for creature in self.positionToCreature.values()])) <= 1

	def isEmpty(self, position):
		return position in self.allPositions and position not in self.positionToCreature

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

# Sort key for positions (x,y), to be sorted in reading order.
# Pass this function as "key" argument to sorted(listToSort, key=positionSortKey)
def positionSortKey(position):
	return (position[1], position[0])
