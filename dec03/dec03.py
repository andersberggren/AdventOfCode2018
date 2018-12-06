###########
# Classes #
###########
class Claim:
	def __init__(self, id, x, y, width, height):
		self.id = id
		self.x = int(x)
		self.y = int(y)
		self.width = int(width)
		self.height = int(height)

	def toString(self):
		s = "Claim[id={id},x={x},y={y},width={width},height={height}]"
		s = s.format(id=self.id, x=self.x, y=self.y, width=self.width, height=self.height)
		return s

	# String format: #<ID> @ <x>,<y>: <width>x<height>
	# Ex: #1 @ 520,746: 4x20
	@staticmethod
	def createFromString(s):
		id = s.split()[0][1:]
		position = s.split("@")[1].split(":")[0]
		x = position.split(",")[0].strip()
		y = position.split(",")[1].strip()
		size = s.split()[3]
		width =  size.split("x")[0].strip()
		height = size.split("x")[1].strip()
		return Claim(id, x, y, width, height)

#############
# Functions #
#############
# Reads a file, and returns a list of Claim
def getClaimsFromFile(fileName):
	claims = []
	with open(fileName) as f:
		for line in f.readlines():
			claims.append(Claim.createFromString(line))
	return claims

# Combines the claims in 'claims', and returns a dict,
# where the key is a position typle (x,y),
# and the value is the number of claims on that square.
def getCombinedClaims(claims):
	combinedClaims = {}
	for claim in claims:
		for x in range(claim.x, claim.x+claim.width):
			for y in range(claim.y, claim.y+claim.height):
				position = (x, y)
				try:
					combinedClaims[position] += 1
				except KeyError:
					# This key did not previously exist. Initialize to 1.
					combinedClaims[position] = 1
	return combinedClaims

def getNumberOfOverlappingSquares(combinedClaims):
	count = 0
	for value in combinedClaims.values():
		if value > 1:
			count += 1
	return count

def findNonOverlappingClaims(combinedClaims, claims):
	nonOverlappingClaims = []
	for claim in claims:
		isOverlapping = False
		for x in range(claim.x, claim.x+claim.width):
			for y in range(claim.y, claim.y+claim.height):
				position = (x, y)
				if combinedClaims[position] > 1:
					isOverlapping = True
		if not isOverlapping:
			nonOverlappingClaims.append(claim)
	return nonOverlappingClaims

########
# Main #
########
claims = getClaimsFromFile("input03")
combinedClaims = getCombinedClaims(claims)

# Part 1: How many squares are claimed by more than one elf?
numberOfOverlappingSquares = getNumberOfOverlappingSquares(combinedClaims);
print("Number of squares with more than one claim: {}".format(numberOfOverlappingSquares))

# Part 2: What is the ID of the only claim that is not overlapping with any other claim?
nonOverlappingClaims = findNonOverlappingClaims(combinedClaims, claims)
print("Found {} overlapping claim(s):".format(len(nonOverlappingClaims)))
for claim in nonOverlappingClaims:
	print(claim.toString())
