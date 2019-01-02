import sys

class Cave:
	def __init__(self, depth, targetLocation):
		self.depth = depth
		self.targetLocation = targetLocation
		self.locationToRegion = {}
		self.createRegions()

	def createRegions(self):
		for x in range(self.targetLocation[0]+1):
			for y in range(self.targetLocation[1]+1):
				self.createRegion((x,y))

	def createRegion(self, location):
		region = Region(location)
		self.locationToRegion[location] = region
		region.geologicIndex = self.getGeologicIndex(location)
		region.erosionLevel = (region.geologicIndex+self.depth) % 20183
		region.type = RegionType.getRegionType(region.erosionLevel)
		return region

	# Returns the Region at "location". Creates the Region if it doesn't already exist.
	def getRegion(self, location):
		try:
			return self.locationToRegion[location]
		except KeyError:
			return self.createRegion(location)
	
	def getGeologicIndex(self, location):
		(x,y) = location
		if location == (0,0):
			return 0
		elif location == self.targetLocation:
			return 0
		elif y == 0:
			return x * 16807
		elif x == 0:
			return y * 48271
		else:
			return self.getErosionLevel((x-1,y)) * self.getErosionLevel((x,y-1))

	def getErosionLevel(self, location):
		return self.getRegion(location).erosionLevel

	def getRisk(self, location):
		return self.getRegion(location).type.risk
	
	def getTotalRisk(self):
		xRange = range(self.targetLocation[0]+1)
		yRange = range(self.targetLocation[1]+1)
		return sum([self.locationToRegion[(x,y)].type.risk for x in xRange for y in yRange])

	def getValidTools(self, location):
		return self.getRegion(location).type.validTools
	
	def getCommonTool(self, locationA, locationB):
		commonTools = self.getValidTools(locationA) & self.getValidTools(locationB)
		if len(commonTools) != 1:
			raise RuntimeError("Location {a} and {b} have {n} tools in common. Expected 1.". format(
					a=locationA, b=locationB, n=len(commonTools)))
			print("Location {a} and {b} have {n} tools in common. Expected 1.". format(
					a=locationA, b=locationB, n=len(commonTools)))
			sys.exit(1)
		return commonTools.pop()
	
	def printCave(self):
		for y in range(self.targetLocation[1]+6):
			for x in range(self.targetLocation[0]+6):
				location = (x,y)
				symbol = self.getRegion(location).type.symbol
				if location == (0,0):
					symbol = "M"
				elif location == self.targetLocation:
					symbol = "T"
				print(symbol, end="")
			print()

class Tool:
	def __init__(self, name):
		self.name = name

Tool.empty = Tool("Empty")
Tool.torch = Tool("Torch")
Tool.climbingGear = Tool("Climbing gear")

class Region:
	def __init__(self, location):
		self.location = location
		self.geologicIndex = None
		self.erosionLevel = None
		self.type = None

class RegionType:
	def __init__(self, symbol, risk, validTools):
		self.symbol = symbol
		self.risk = risk
		self.validTools = validTools
	
	@staticmethod
	def getRegionType(erosionLevel):
		return RegionType.all[erosionLevel % 3]

RegionType.rocky  = RegionType(".", 0, {Tool.torch, Tool.climbingGear})
RegionType.wet    = RegionType("=", 1, {Tool.empty, Tool.climbingGear})
RegionType.narrow = RegionType("|", 2, {Tool.empty, Tool.torch})
RegionType.all = [RegionType.rocky, RegionType.wet, RegionType.narrow]
