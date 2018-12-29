import re

###########
# Classes #
###########
class Army:
	def __init__(self, faction):
		self.faction = faction
		self.groups = []

class Group:
	def __init__(self, army, nrUnits, hpPerUnit, defenseModifiers,
	             attackPowerPerUnit, attackType, initiative):
		self.army = army
		self.nrUnits = nrUnits
		self.hpPerUnit = hpPerUnit
		self.defenseModifiers = defenseModifiers
		self.attackPowerPerUnit = attackPowerPerUnit
		self.attackType = attackType
		self.initiative = initiative
	
	def getEffectivePower(self):
		return self.nrUnits * self.attackPowerPerUnit
	
	def printGroup(self):
		message = "{units} units, {hp} HP/unit, defense modifiers {dm}, " \
				+ "{ap} attack power, attack type {at}, {i} initiative"
		print(message.format(units=self.nrUnits, hp=self.hpPerUnit, dm=self.defenseModifiers,
		                     ap=self.attackPowerPerUnit, at=self.attackType, i=self.initiative))

#############
# Functions #
#############
def getArmiesFromFile(fileName):
	with open(fileName) as f:
		armies = []
		army = None
		for line in f.readlines():
			factionMatch = re.match("^([A-Za-z ]+):$", line)
			groupMatch = re.match("^(?P<nrunits>\d+) units each with (?P<hp>\d+) hit points " \
					+ "(?P<defensemodifiers>\(.*\) )?with an attack that does " \
					+ "(?P<ap>\d+) (?P<attacktype>\w+) damage at " \
					+ "initiative (?P<initiative>\d+)", line)
			if factionMatch:
				army = Army(factionMatch.group(1))
				armies.append(army)
			elif groupMatch:
				nrUnits = int(groupMatch.group("nrunits"))
				hpPerUnit = int(groupMatch.group("hp"))
				defenseModifiers = getDefenseModifiers(groupMatch.group("defensemodifiers"))
				attackPowerPerUnit = int(groupMatch.group("ap"))
				attackType = groupMatch.group("attacktype")
				initiative = int(groupMatch.group("initiative"))
				group = Group(army, nrUnits, hpPerUnit, defenseModifiers,
				              attackPowerPerUnit, attackType, initiative)
				army.groups.append(group)
				group.id = army.faction + " " + str(len(army.groups))
		return armies

# Returns a dict. Key is damage type. Value is modifier.
def getDefenseModifiers(descriptionString):
	if descriptionString is None:
		return {}
	defenseModifiers = {}
	for s in descriptionString.strip("() ").split(";"):
		match = re.match("(\w+) to (.*)", s.strip())
		modifierType = match.group(1)
		if modifierType == "immune":
			modifier = 0
		elif modifierType == "weak":
			modifier = 2
		else:
			raise ValueError("Unknown modifier type: {}".format(modifierType))
		for attackType in match.group(2).split(","):
			defenseModifiers[attackType.strip()] = modifier
	return defenseModifiers

def getTargetSelections(armies):
	print("Target selection:")
	attackerToDefender = {}
	for attacker in getGroupsInTargetSelectionOrder(armies):
		eligibleDefenders = getEnemyGroups(armies, attacker)
		eligibleDefenders = [x for x in eligibleDefenders if x not in attackerToDefender.values()]
		defender = getTarget(attacker, eligibleDefenders)
		if defender is not None:
			attackerToDefender[attacker] = defender
			print("{a} has {ep} effective power, selects {d}".format(
					a=attacker.id, ep=attacker.getEffectivePower(), d=defender.id))
		else:
			print("{a} has {ep} effective power, but no eligible targets :(".format(
					a=attacker.id, ep=attacker.getEffectivePower()))
	return sorted([x for x in attackerToDefender.items()], key=lambda x: x[0].initiative, reverse=True)

def getGroupsInTargetSelectionOrder(armies):
	def sortKey(group):
		return (group.getEffectivePower(), group.initiative)
	return sorted([group for army in armies for group in army.groups], key=sortKey, reverse=True)

def getTarget(attacker, defenderGroups):
	def sortKey(defender):
		return (getDamage(attacker, defender), defender.getEffectivePower(), defender.initiative)
	defenderGroups = [x for x in defenderGroups if getDamage(attacker, x) > 0]
	defenderGroups = sorted(defenderGroups, key=sortKey, reverse=True)
	try:
		return defenderGroups[0]
	except IndexError:
		return None

def getEnemyGroups(armies, myGroup):
	return [group for army in armies for group in army.groups if army != myGroup.army]

def getDamage(attacker, defender):
	try:
		modifier = defender.defenseModifiers[attacker.attackType]
	except KeyError:
		modifier = 1
	return attacker.attackPowerPerUnit * attacker.nrUnits * modifier

def doOneRoundOfAttacks(armies):
	attackersAndDefenders = getTargetSelections(armies)
	print("Attack:")
	for (attacker, defender) in attackersAndDefenders:
		damageDealt = max(getDamage(attacker, defender), 0)
		unitsKilled = damageDealt // defender.hpPerUnit
		defender.nrUnits -= unitsKilled
		print("{a} attacks {d}, dealing {dp} damage, killing {u} units".format(
				a=attacker.id, d=defender.id, dp=damageDealt, u=unitsKilled))
		if defender.nrUnits <= 0:
			defender.army.groups.remove(defender)
			print("{} has no units left".format(defender.id))

########
# Main #
########
# Part 1
armies = getArmiesFromFile("input24.txt")
while len([army for army in armies if len(army.groups) > 0]) == 2:
	doOneRoundOfAttacks(armies)
remainingUnits = sum([group.nrUnits for army in armies for group in army.groups])
print("Remaining units: {}".format(remainingUnits))

# Part 2
armies = getArmiesFromFile("input24.txt")
# Boost immune system
# High (maybe too high): 34
# Too low: 33
for army in armies:
	if army.faction == "Immune System":
		for group in army.groups:
			group.attackPowerPerUnit += 34
while len([army for army in armies if len(army.groups) > 0]) == 2:
	doOneRoundOfAttacks(armies)
remainingUnits = sum([group.nrUnits for army in armies for group in army.groups])
print("Remaining units: {}".format(remainingUnits))
