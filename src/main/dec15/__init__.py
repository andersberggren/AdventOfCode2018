from aoclib.filereader import getFileAsSingleString
from dec15.world import World, Creature, positionSortKey

#############
# Functions #
#############
def doOneRoundOfActions(world):
	for creature in world.getCreaturesSortedByExecutionOrder():
		if creature.hitPoints > 0:
			creatureMove(world, creature)
			creatureAttack(world, creature)

def doCombat(world):
	rounds = 0
	while True:
		doOneRoundOfActions(world)
		if world.isCombatOver():
			hitPointsLeft = sum([x.hitPoints for x in world.positionToCreature.values()])
			return rounds * hitPointsLeft
		else:
			rounds += 1

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

def part1():
	world = World.createFromString(getFileAsSingleString("input15.txt"))
	result = doCombat(world)
	print("Part 1 outcome: {}".format(result))

def part2():
	worldAsString = getFileAsSingleString("input15.txt")
	lowValue = Creature((0,0), "Elf").attackPower
	highValue = None
	highValueOutcome = None
	while highValue is None or highValue-lowValue > 1:
		world = World.createFromString(worldAsString)
		if highValue is None:
			elfAttackPower = 1
			while elfAttackPower <= lowValue:
				elfAttackPower *= 2
		else:
			elfAttackPower = ((lowValue+1)+(highValue-1)) // 2
		elves = [x for x in world.positionToCreature.values() if x.type == "Elf"]
		for elf in elves:
			elf.attackPower = elfAttackPower
		print("Elf attack power: {}".format(elfAttackPower))
		
		outcome = doCombat(world)
		allElvesSurvived = all(elf.hitPoints > 0 for elf in elves)
		if allElvesSurvived:
			highValue = elfAttackPower
			highValueOutcome = outcome
			print("All elves survived!")
		else:
			lowValue = elfAttackPower
			print("An elf died!")
	print("Part 2 outcome: {}".format(highValueOutcome))

########
# Main #
########
if __name__ == "__main__":
	part1()
	part2()
