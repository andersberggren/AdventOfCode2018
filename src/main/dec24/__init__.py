from aoclib.filereader import getFileAsSingleString
from dec24.parser import getArmiesFromString

# Returns a list of Group, sorted by the order in which groups should select targets.
def getGroupsInTargetSelectionOrder(armies):
	def sortKey(group):
		return (group.getEffectivePower(), group.initiative)
	return sorted([group for army in armies for group in army.groups], key=sortKey, reverse=True)

# Returns a list of (attacker, defender), sorted by order of attack.
# The Group with the highest initiative attacks first.
def getGroupsInAttackOrder(attackersAndDefenders):
	return sorted([x for x in attackersAndDefenders], key=lambda x: x[0].initiative, reverse=True)

# Returns a list of (attacker, defender), sorted by the order in which groups should attack.
def getTargetSelections(armies):
	attackerToDefender = {}
	for attacker in getGroupsInTargetSelectionOrder(armies):
		eligibleDefenders = getEnemyGroups(armies, attacker)
		eligibleDefenders = [x for x in eligibleDefenders if x not in attackerToDefender.values()]
		defender = getTargetSelection(attacker, eligibleDefenders)
		if defender is not None:
			attackerToDefender[attacker] = defender
	return getGroupsInAttackOrder(attackerToDefender.items())

def getTargetSelection(attacker, defenderGroups):
	def sortKey(defender):
		return (attacker.calcDamage(defender), defender.getEffectivePower(), defender.initiative)
	defenderGroups = [x for x in defenderGroups if attacker.calcDamage(x) > 0]
	defenderGroups = sorted(defenderGroups, key=sortKey, reverse=True)
	try:
		return defenderGroups[0]
	except IndexError:
		return None

def getEnemyGroups(armies, myGroup):
	return [group for army in armies for group in army.groups if army != myGroup.army]

# Returns True iff at least one unit was killed, i.e. some progress was made.
def fightOneRound(armies):
	return any([attacker.attack(defender) for (attacker, defender) in getTargetSelections(armies)])

# Returns (winningArmy, remainingUnits), or (None, None) if no one will ever win.
def fightUntilThereIsOnlyOneArmyLeft(armies):
	while len([army for army in armies if len(army.groups) > 0]) > 1:
		progress = fightOneRound(armies)
		if not progress:
			return (None, None)
	winningArmy = next(army for army in armies if len(army.groups) > 0)
	remainingUnits = sum([group.nrUnits for group in winningArmy.groups])
	return (winningArmy, remainingUnits)

# Finds minimum boost required for the immune system to win.
# Returns (minimumBoost, remainingUnits).
def findMinimumBoost(inputFileAsString):
	factionBeingBoosted = "Immune System"
	lowValue = 0
	highValue = None
	highValueRemainingUnits = None
	while highValue is None or highValue-lowValue > 1:
		armies = getArmiesFromString(inputFileAsString)
		if highValue is None:
			boostValue = max(lowValue, 1) * 2
		else:
			boostValue = ((lowValue+1)+(highValue-1)) // 2
		for army in armies:
			if army.faction == factionBeingBoosted:
				army.boostAttackPowerPerUnit(boostValue)
		(winningArmy, remainingUnits) = fightUntilThereIsOnlyOneArmyLeft(armies)
		print("With boostValue={b}, {a} wins, with {u} remaining units".format(
				b=boostValue, a=winningArmy, u=remainingUnits))
		if winningArmy is not None and winningArmy.faction == factionBeingBoosted:
			highValue = boostValue
			highValueRemainingUnits = remainingUnits
		else:
			lowValue = boostValue
	return (highValue, highValueRemainingUnits)

if __name__ == "__main__":
	inputFileAsString = getFileAsSingleString("input24.txt")
	armies = getArmiesFromString(inputFileAsString)
	(winningArmy, remainingUnits) = fightUntilThereIsOnlyOneArmyLeft(armies)
	print("Part 1: {a} wins, with {u} remaining units".format(a=winningArmy, u=remainingUnits))
	(minimumBoost, remainingUnits) = findMinimumBoost(inputFileAsString)
	print("Part 2: Minimum boost is {b}. Immune system wins with {u} remaining units.".format(
			b=minimumBoost, u=remainingUnits))
