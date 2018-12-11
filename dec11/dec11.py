#############
# Functions #
#############
def calcPowerLevel(x, y, serialNumber):
	rackID = x + 10
	powerLevel = rackID * y
	powerLevel += serialNumber
	powerLevel *= rackID
	powerLevel = (powerLevel//100) % 10
	powerLevel -= 5
	return powerLevel

def calcPowerLevel3x3(x, y, coordToPowerLevel):
	return sum([coordToPowerLevel[(xIter,yIter)] for xIter in range(x, x+3) for yIter in range(y, y+3)])

########
# Main #
########
serialNumber = 1308
minX = 1
maxX = 300
minY = 1
maxY = 300

coordToPowerLevel = {}
for x in range(minX, maxX+1):
	for y in range(minY, maxY+1):
		coordToPowerLevel[(x,y)] = calcPowerLevel(x, y, serialNumber)

coordToPowerLevel3x3 = {}
for x in range(minX, maxX-1):
	for y in range(minY, maxY-1):
		coordToPowerLevel3x3[(x,y)] = calcPowerLevel3x3(x, y, coordToPowerLevel)

(coord, powerLevel) = sorted(coordToPowerLevel3x3.items(), key=lambda item: item[1], reverse=True)[0]
print("3x3 square at {coord} has highest power level: {pl}".format(coord=coord, pl=powerLevel))
