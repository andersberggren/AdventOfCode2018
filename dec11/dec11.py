###########
# Classes #
###########
class Grid:
	def __init__(self, width, height, serialNumber):
		self.width = width
		self.height = height
		self.serialNumber = serialNumber
		self.coordToPowerLevel = {}
		for x in range(1, width+1):
			for y in range(1, height+1):
				self.coordToPowerLevel[(x,y)] = self.calcPowerLevel(x, y)

	def calcPowerLevel(self, x, y):
		rackID = x + 10
		powerLevel = ((rackID*y) + self.serialNumber) * rackID
		powerLevel = (powerLevel//100) % 10 - 5
		return powerLevel

	def calcPowerLevelAggregated(self, topLeftX, topLeftY, size):
		xRange = range(topLeftX, topLeftX+size)
		yRange = range(topLeftY, topLeftY+size)
		return sum([self.coordToPowerLevel[(x,y)] for x in xRange for y in yRange])

	# Returns (coordinate, totalPower).
	def getLargestTotalPower(self, size):
		coordToTotalPower = {}
		for x in range(1, grid.width+2-size):
			for y in range(1, grid.height-+2-size):
				coordToTotalPower[(x,y)] = self.calcPowerLevelAggregated(x, y, size)
		return sorted(coordToTotalPower.items(), key=lambda x: x[1], reverse=True)[0]

#############
# Functions #
#############

########
# Main #
########
grid = Grid(300, 300, 1308)

# Part 1
(coord, powerLevel) = grid.getLargestTotalPower(3)
print("3x3 square at {coord} has highest power level: {pl}".format(coord=coord, pl=powerLevel))

# Part 2
# Brute force solution. Execution time increases as size of square increases.
# At square size ~50x50, execution is awfully slow.
# The largest total power at this point was a 19x19 square.
# I submitted that, and it turned out to be right, but I didn't know that before I submitted it,
# because all square sizes hadn't been evaluated.
# Performance can be improved by re-using values calculated for previous smaller squares.
for i in range(1, grid.width+1):
	(coord, powerLevel) = grid.getLargestTotalPower(i)
	print("{i}x{i} square at {coord} has highest power level: {pl}".format(
			i=i, coord=coord, pl=powerLevel), flush=True)
