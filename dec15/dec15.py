###########
# Classes #
###########
# Elf or goblin
class Creature:
	def __init__(self, position, type):
		self.position = position
		self.type = type
		self.hitpoints = 200

class World:
	def __init__(self):
		self.allPositions = set()
		self.positionToCreature = {}

	def addPosition(self, position):
		self.allPositions.add(position)

	def addCreature(self, creature):
		self.positionToCreature[creature.position] = creature

	def getCreaturesSortedByExecutionOrder(self):
		sortKey = lambda x: (x.position[1], x.position[0])
		return sorted(self.positionToCreature.values(), key=sortKey)

	def getEnemies(self, friendType):
		return [x for x in self.positionToCreature.values() if x.type != friendType]

	def getAdjacentSquares(self, position):
		(x,y) = position
		positions = [(x,y+1), (x,y-1), (x+1,y), (x-1,y)]
		return [p for p in positions if p in self.allPositions]

	def getAdjacentEmptySquares(self, position):
		return [p for p in self.getAdjacentSquares(position) if self.isEmpty(p)]

	def isCombatOver(self):
		# Combat is over if there is only one creature type left
		return len(set([creature.type for creature in self.positionToCreature.values()])) <= 1

	def isEmpty(self, position):
		return position in self.allPositions and position not in self.positionToCreature

	def isReachable(self, positionFrom, positionTo):
		evaluated = set()
		leftToEvaluate = set(self.getAdjacentEmptySquares(positionFrom))
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
		# Move:
		# - If adjacent to enemy, do nothing.
		# - If there exists a reachable square adjacent to an enemy,
		#   move one step towards the closest reachable square.
		if not world.existsAdjacentEnemy(creature):
			enemies = world.getEnemies(creature.type)
			enemyAdjacentSquares = set([world.getAdjacentSquares(x.position) for x in enemies])
			pass
		# TODO Attack
		# ...

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
				if world.isReachable((1,11), position):
					symbol = "R"
				else:
					symbol = "."
			print(symbol, end="")
		print()

########
# Main #
########
if __name__ == "__main__":
	world = readWorldFromFile("input15")
	print()
	printWorld(world)
