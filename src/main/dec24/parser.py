import re

from dec24.classes import Army, Group

# Returns a list of Army.
def getArmiesFromString(s):
	armies = []
	army = None
	for line in s.splitlines():
		factionMatch = re.match("^([A-Za-z ]+):$", line)
		groupMatch = re.match("^(?P<nrunits>\d+) units each with (?P<hp>\d+) hit points " \
				+ "(?P<defensemodifiers>\(.*\) )?with an attack that does " \
				+ "(?P<ap>\d+) (?P<attacktype>\w+) damage at " \
				+ "initiative (?P<initiative>\d+)", line)
		if factionMatch:
			army = Army(factionMatch.group(1))
			armies.append(army)
		elif groupMatch:
			name = army.faction + " " + str(len(army.groups)+1)
			nrUnits = int(groupMatch.group("nrunits"))
			hpPerUnit = int(groupMatch.group("hp"))
			defenseModifiers = getDefenseModifiers(groupMatch.group("defensemodifiers"))
			attackPowerPerUnit = int(groupMatch.group("ap"))
			attackType = groupMatch.group("attacktype")
			initiative = int(groupMatch.group("initiative"))
			group = Group(name, army, nrUnits, hpPerUnit, defenseModifiers,
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
