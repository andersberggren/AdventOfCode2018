import re

from aoclib.filereader import getFileAsListOfString

###########
# Classes #
###########
class Claim:
	def __init__(self, nr, x, y, width, height):
		self.nr = nr
		self.x = x
		self.y = y
		self.width = width
		self.height = height

	def __repr__(self):
		return "Claim[nr={nr},x={x},y={y},width={width},height={height}]".format(
				nr=self.nr, x=self.x, y=self.y, width=self.width, height=self.height)

	# String format: #<ID> @ <x>,<y>: <width>x<height>
	# Ex: #1 @ 520,746: 4x20
	@staticmethod
	def createFromString(s):
		match = re.match("^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", s)
		nr     = int(match.group(1))
		x      = int(match.group(2))
		y      = int(match.group(3))
		width  = int(match.group(4))
		height = int(match.group(5))
		return Claim(nr, x, y, width, height)

#############
# Functions #
#############
# Returns a dict, where key is position (x,y), and value is number of claims on that square.
def getPositionToNrClaims(claims):
	positionToNrClaims = {}
	for claim in claims:
		for x in range(claim.x, claim.x+claim.width):
			for y in range(claim.y, claim.y+claim.height):
				position = (x, y)
				try:
					positionToNrClaims[position] += 1
				except KeyError:
					positionToNrClaims[position] = 1
	return positionToNrClaims

def findNonOverlappingClaim(positionToNrClaims, claims):
	for claim in claims:
		xRange = range(claim.x, claim.x+claim.width)
		yRange = range(claim.y, claim.y+claim.height)
		if not any(1 for x in xRange for y in yRange if positionToNrClaims[(x,y)] > 1):
			return claim

########
# Main #
########
claims = [Claim.createFromString(line) for line in getFileAsListOfString("input03.txt")]
positionToNrClaims = getPositionToNrClaims(claims)

# Part 1: How many squares are claimed by more than one elf?
numberOfOverlappingSquares = len([1 for x in positionToNrClaims.values() if x > 1])
print("Number of squares with more than one claim: {}".format(numberOfOverlappingSquares))

# Part 2: What is the ID of the only claim that is not overlapping with any other claim?
nonOverlappingClaim = findNonOverlappingClaim(positionToNrClaims, claims)
print("Found non-overlapping claim: {}".format(nonOverlappingClaim))
