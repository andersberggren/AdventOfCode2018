###########
# Classes #
###########
class UnreachableError(Exception):
	pass

# Elf or goblin
class Creature:
	def __init__(self, position, type):
		self.position = position
		self.type = type
		self.attackPower = 3
		self.hitPoints = 200

class World:
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

#############
# Functions #
#############
def readWorldFromFile(fileName):
	openPositionSymbols = set([".", "E", "G"])
	world = World()
	with open(fileName) as f:
		lines = f.readlines()
		for y in range(len(lines)):
			line = lines[y].strip()
			for x in range(len(line)):
				position = (x,y)
				symbol = line[x]
				if symbol in openPositionSymbols:
					world.addPosition(position)
				if symbol == "E":
					world.addCreature(Creature(position, "Elf"))
				elif symbol == "G":
					world.addCreature(Creature(position, "Goblin"))
				print(symbol, end="")
			print()
	return world

def doOneRoundOfActions(world):
	for creature in world.getCreaturesSortedByExecutionOrder():
		if creature.hitPoints > 0:
			creatureMove(world, creature)
			creatureAttack(world, creature)

# Moves creatures, according to:
# 1. If adjacent to enemy, do nothing.
# 2. If there exists a reachable square adjacent to an enemy,
#    move one step towards the closest reachable square.
def creatureMove(world, creature):
	if world.existsAdjacentEnemy(creature):
		return
	enemies = world.getEnemies(creature.type)
	candidateSquares = set()
	for enemy in enemies:
		candidateSquares |= world.getAdjacentEmptySquares(enemy.position)
	candidateSquares = set([x for x in candidateSquares if world.isReachable(creature.position, x)])
	if not candidateSquares:
		return
	distancesAndPositions = [(x, world.getDistance(creature.position, x)) for x in candidateSquares]
	minDistance = min([x[1] for x in distancesAndPositions])
	candidateSquares = [x[0] for x in distancesAndPositions if x[1] == minDistance]
	targetSquare = sorted(candidateSquares, key=positionSortKey)[0]
	
	adjacentSquares = world.getAdjacentEmptySquares(creature.position)
	distancesAndPositions = [(x, world.getDistance(x, targetSquare)) for x in adjacentSquares if world.isReachable(x, targetSquare)]
	minDistance = min([x[1] for x in distancesAndPositions])
	candidateSquares = [x[0] for x in distancesAndPositions if x[1] == minDistance]
	moveTo = sorted(candidateSquares, key=positionSortKey)[0]
	world.moveCreature(creature, moveTo)

def creatureAttack(world, creature):
	adjacentSquares = world.getAdjacentSquares(creature.position)
	adjacentEnemies = [x for x in world.getEnemies(creature.type) if x.position in adjacentSquares]
	if not adjacentEnemies:
		return
	# Sort by hit points
	adjacentEnemies = sorted(adjacentEnemies, key=lambda x: x.hitPoints)
	adjacentEnemies = [x for x in adjacentEnemies if x.hitPoints == adjacentEnemies[0].hitPoints]
	# Sort by reading order
	targetEnemy = sorted(adjacentEnemies, key=lambda x: positionSortKey(x.position))[0]
	world.attackCreature(creature, targetEnemy)

# Sort key for positions (x,y), to be sorted in reading order.
# Pass this function as "key" argument to sorted(listToSort, key=positionSortKey)
def positionSortKey(position):
	return (position[1], position[0])

# Temp debug
def printWorld(world):
	maxX = max([pos[0] for pos in world.allPositions])
	maxY = max([pos[1] for pos in world.allPositions])
	for y in range(maxY+2):
		for x in range(maxX+2):
			position = (x,y)
			symbol = "#"
			if position in world.positionToCreature:
				symbol = world.positionToCreature[position].type[0]
			elif position in world.allPositions:
				symbol = "."
			print(symbol, end="")
		print()

########
# Main #
########
if __name__ == "__main__":
	world = readWorldFromFile("input15")
	rounds = 0
	while True:
		doOneRoundOfActions(world)
		if world.isCombatOver():
			hitPointsLeft = sum([x.hitPoints for x in world.positionToCreature.values()])
			print("Outcome: {}".format(rounds * hitPointsLeft))
			break
		else:
			rounds += 1
			printWorld(world)
			print("Rounds completed: {}".format(rounds), flush=True)
