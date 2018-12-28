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

########
# Main #
########
armies = getArmiesFromFile("input24.txt")
for army in armies:
	print("Faction: " + army.faction)
	print("Number of groups: {}".format(len(army.groups)))
	for group in army.groups:
		group.printGroup()
