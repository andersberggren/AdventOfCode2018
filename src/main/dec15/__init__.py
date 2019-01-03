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
	moveToCandidates = {
		p for enemy in world.getEnemies(creature.type)
		for p in world.getAdjacentEmptySquares(enemy.position)
	}
	moveTo = world.getClosestReachableSquare(creature.position, moveToCandidates)
	if moveTo is None:
		return
	adjacentSquares = world.getAdjacentEmptySquares(creature.position)
	nextStep = world.getClosestReachableSquare(moveTo, adjacentSquares)
	world.moveCreature(creature, nextStep)

def creatureAttack(world, creature):
	targetEnemy = world.getAdjacentEnemy(creature)
	if targetEnemy is not None:
		world.attackCreature(creature, targetEnemy)

def part1(worldAsString):
	world = World.createFromString(worldAsString)
	outcome = doCombat(world)
	print("Part 1 outcome: {}".format(outcome))

def part2(worldAsString):
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
		print("Elf attack power {l} is too low, {h} is high enough. Now try {t}...".format(
			l=lowValue, h=highValue, t=elfAttackPower))
		
		outcome = doCombat(world)
		allElvesSurvived = all(elf.hitPoints > 0 for elf in elves)
		if allElvesSurvived:
			highValue = elfAttackPower
			highValueOutcome = outcome
		else:
			lowValue = elfAttackPower
	print("Lowest attack power with all elves surviving: {}".format(highValue))
	print("Part 2 outcome: {}".format(highValueOutcome))

########
# Main #
########
if __name__ == "__main__":
	worldAsString = getFileAsSingleString("input15.txt")
	part1(worldAsString)
	part2(worldAsString)
