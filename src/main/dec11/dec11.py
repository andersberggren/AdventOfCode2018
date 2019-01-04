###########
# Classes #
###########
class Grid:
	def __init__(self, size, serialNumber):
		self.size = size
		self.serialNumber = serialNumber
		# Dict, key is cell coordinate (x,y), value is power level.
		self.cellToPowerLevel = {}
		for x in range(1, size+1):
			for y in range(1, size+1):
				self.cellToPowerLevel[(x,y)] = self.calcPowerLevelForSingleCell(x, y)
		# Dict, key is top-left coordinate and size (x,y,size), value is total power.
		self.squareToTotalPower = {}

	# Returns the power level for the cell at (x,y).
	def calcPowerLevelForSingleCell(self, x, y):
		rackID = x + 10
		powerLevel = ((rackID*y) + self.serialNumber) * rackID
		powerLevel = (powerLevel//100) % 10 - 5
		return powerLevel

	# Returns the total power of the square with size squareSize and
	# top-left coordinate (topLeftX, topLeftY).
	def calcTotalPowerInSquare(self, topLeftX, topLeftY, squareSize):
		totalPower = 0
		if squareSize == 1:
			totalPower = self.cellToPowerLevel[(topLeftX,topLeftY)]
			self.squareToTotalPower[(topLeftX,topLeftY,squareSize)] = totalPower
			return totalPower

		# Which strategy requires the fewest lookups?
		divisor = getLargestDivisorSmallerThanSelf(squareSize)
		defaultStrategy = squareSize * 2
		alternativeStrategy = (squareSize//divisor) ** 2
		if defaultStrategy <= alternativeStrategy:
			# Default strategy:
			# Get total power of square that is 1 size smaller,
			# then add the power levels of the cells along the right and bottom edge.
			totalPower = self.squareToTotalPower[(topLeftX, topLeftY, squareSize-1)]
			for x in range(topLeftX, topLeftX+squareSize):
				y = topLeftY + squareSize - 1
				totalPower += self.cellToPowerLevel[(x,y)]
			for y in range(topLeftY, topLeftY+squareSize-1):
				x = topLeftX + squareSize - 1
				totalPower += self.cellToPowerLevel[(x,y)]
		else:
			# Alternative strategy:
			# Get total power from smaller sub-squares that have already been calculated.
			for x in range(topLeftX, topLeftX+squareSize, divisor):
				for y in range(topLeftY, topLeftY+squareSize, divisor):
					totalPower += self.squareToTotalPower[(x,y,divisor)]
		self.squareToTotalPower[(topLeftX,topLeftY,squareSize)] = totalPower
		return totalPower

	# Returns ((x,y), totalPower).
	def getLargestTotalPower(self, squareSize):
		# Make sure we have calculated and cached the total power for square sizes <= squareSize.
		for i in range(1, squareSize+1):
			if (1,1,i) not in self.squareToTotalPower:
				for x in range(1, self.size+2-i):
					for y in range(1, self.size+2-i):
						self.calcTotalPowerInSquare(x, y, i)
		items = [x for x in self.squareToTotalPower.items() if x[0][2] == squareSize]
		((x, y, size), totalPower) = sorted(items, key=lambda item: item[1], reverse=True)[0]
		return ((x,y), totalPower)

#############
# Functions #
#############
def getLargestDivisorSmallerThanSelf(x):
	largestDivisor = 1
	for divisor in range(1, x):
		if x % divisor == 0:
			largestDivisor = divisor
	return largestDivisor

def findLargestTotalPower(grid):
	sizeCoordTotalPower = []
	for i in range(1, grid.size+1):
		if canSkip(i, sizeCoordTotalPower):
			print("Skipping {i}x{i}".format(i=i))
			continue
		(coord, totalPower) = grid.getLargestTotalPower(i)
		sizeCoordTotalPower.append((i, coord, totalPower))
		print("Among all {i}x{i} squares, the one at {coord} has the highest total power: {tp}".format(
				i=i, coord=coord, tp=totalPower), flush=True)
		bestSoFar = sorted(sizeCoordTotalPower, key=lambda x: x[2], reverse=True)[0]
		print("So far, the {size}x{size} square at {coord} has the highest total power: {tp}".format(
				size=bestSoFar[0], coord=bestSoFar[1], tp=bestSoFar[2]), flush=True)

def canSkip(squareSize, sizeCoordTotalPower):
	if not sizeCoordTotalPower:
		return False
	toBeat = sorted(sizeCoordTotalPower, key=lambda x: x[2], reverse=True)[0][2]
	return any(
		squareSize % subSquareSize == 0 and (squareSize//subSquareSize)**2 * totalPower < toBeat
		for (subSquareSize, coord, totalPower) in sizeCoordTotalPower  # @UnusedVariable
	)

########
# Main #
########
if __name__ == '__main__':
	findLargestTotalPower(Grid(300, 1308))
