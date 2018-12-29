class Army:
	def __init__(self, faction):
		self.faction = faction
		self.groups = []
	
	def boostAttackPowerPerUnit(self, boostValue):
		for group in self.groups:
			group.attackPowerPerUnit += boostValue

	def __repr__(self):
		return "Army[faction={}]".format(self.faction)

class Group:
	def __init__(self, name, army, nrUnits, hpPerUnit, defenseModifiers,
	             attackPowerPerUnit, attackType, initiative):
		self.name = name
		self.army = army
		self.nrUnits = nrUnits
		self.hpPerUnit = hpPerUnit
		self.defenseModifiers = defenseModifiers
		self.attackPowerPerUnit = attackPowerPerUnit
		self.attackType = attackType
		self.initiative = initiative
	
	def attack(self, defender):
		damageDealt = max(self.calcDamage(defender), 0)
		unitsKilled = damageDealt // defender.hpPerUnit
		defender.nrUnits -= unitsKilled
		if defender.nrUnits <= 0:
			defender.army.groups.remove(defender)
		return unitsKilled > 0
	
	def getEffectivePower(self):
		return self.nrUnits * self.attackPowerPerUnit
	
	# Returns the damage this group would do if it attacked "defender".
	def calcDamage(self, defender):
		try:
			modifier = defender.defenseModifiers[self.attackType]
		except KeyError:
			modifier = 1
		return self.attackPowerPerUnit * self.nrUnits * modifier
