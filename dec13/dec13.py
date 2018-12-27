###########
# Classes #
###########
class Direction:
	left  = (-1,  0)
	right = ( 1,  0)
	up    = ( 0, -1)
	down  = ( 0,  1)
	all = [left, right, up, down]
	horizontal = [left, right]
	vertical = [up, down]

	@staticmethod
	def getOppositeDirection(direction):
		return (-direction[0], -direction[1])

	@staticmethod
	def getDirectionToTheLeft(direction):
		return (direction[1], -direction[0])

	@staticmethod
	def getDirectionToTheRight(direction):
		return (-direction[1], direction[0])

	@staticmethod
	def getSymbol(directions):
		if all([d in directions for d in Direction.all]):
			return "+"
		elif all([d in directions for d in Direction.horizontal]):
			return "-"
		elif all([d in directions for d in Direction.vertical]):
			return "|"
		elif all([d in directions for d in [Direction.left, Direction.up]]) \
				or all([d in directions for d in [Direction.right, Direction.down]]):
			return "/"
		elif all([d in directions for d in [Direction.left, Direction.down]]) \
				or all([d in directions for d in [Direction.right, Direction.up]]):
			return "\\"
		else:
			raise ValueError("Unknown track section. Directions: {}".format(directions))

	@staticmethod
	def isIntersection(directions):
		return all([d in directions for d in Direction.all])

class Cart:
	symbolToDirection = {
		"<": Direction.left,
		">": Direction.right,
		"^": Direction.up,
		"v": Direction.down
	}
	directionToSymbol = {}
	for (symbol, direction) in symbolToDirection.items():
		directionToSymbol[direction] = symbol

	# Instance variables:
	# position     (x,y)-position.
	# direction    (x,y), where one is 0, and the other is -1 or +1.
	# futureTurns  A list of functions that can be called to turn the Cart.
	#              The first function in the list is called, and then placed last in the list.
	def __init__(self, startPosition, startDirection):
		self.position = startPosition
		self.direction = startDirection
		self.futureTurns = [self.turnLeft, self.turnNot, self.turnRight]

	# Updates the carts position, by moving it one step in the direction it is currently facing.
	def move(self):
		self.position = (self.position[0]+self.direction[0], self.position[1]+self.direction[1])

	# Turns the cart, according to the first applicable rule below:
	# 1. If the cart is at an intersection, it turns according to self.futureTurns
	# 2. If the cart can continue to move forward, it keeps its current direction.
	# 3. The only remaining option is to turn left or right, along the track.
	def turn(self, directions):
		if Direction.isIntersection(directions):
			nextTurn = self.futureTurns.pop(0)
			self.futureTurns.append(nextTurn)
			nextTurn()
		elif self.direction in directions:
			pass
		elif Direction.getDirectionToTheLeft(self.direction) in directions:
			self.turnLeft()
		elif Direction.getDirectionToTheRight(self.direction) in directions:
			self.turnRight()

	def turnLeft(self):
		self.direction = Direction.getDirectionToTheLeft(self.direction)

	def turnRight(self):
		self.direction = Direction.getDirectionToTheRight(self.direction)

	def turnNot(self):
		pass

	def __repr__(self):
		return "Cart[position={p},direction={d}]".format(p=self.position, d=self.direction)

	def __lt__(self, other):
		if self.position[1] < other.position[1]:
			return True
		elif self.position[1] > other.position[1]:
			return False
		else:
			return self.position[0] < other.position[0]

	@staticmethod
	def createCart(startPosition, symbol):
		return Cart(startPosition, Cart.symbolToDirection[symbol])

class TrackSystem:
	def __init__(self):
		self.grid = {}
		self.carts = []

	def addTrackAndOrCart(self, x, y, symbol):
		position = (x,y)
		positionToTheLeft = (x-1,y)
		directions = set()
		if symbol == "|":
			directions.add(Direction.up)
			directions.add(Direction.down)
		elif symbol == "-":
			directions.add(Direction.left)
			directions.add(Direction.right)
		elif symbol == "/":
			if positionToTheLeft in self.grid and Direction.right in self.grid[positionToTheLeft]:
				directions.add(Direction.left)
				directions.add(Direction.up)
			else:
				directions.add(Direction.right)
				directions.add(Direction.down)
		elif symbol == "\\":
			if positionToTheLeft in self.grid and Direction.right in self.grid[positionToTheLeft]:
				directions.add(Direction.left)
				directions.add(Direction.down)
			else:
				directions.add(Direction.right)
				directions.add(Direction.up)
		elif symbol == "+":
			directions.add(Direction.left)
			directions.add(Direction.right)
			directions.add(Direction.up)
			directions.add(Direction.down)
		else:
			cart = Cart.createCart(position, symbol)
			self.carts.append(cart)
			directions.add(cart.direction)
			directions.add(Direction.getOppositeDirection(cart.direction))
		self.grid[(x,y)] = directions

	# Moves all carts one step.
	def tick(self):
		for cart in sorted(self.carts):
			cart.move()
			numberOfCarts = len(self.carts)
			numberOfPositions = len(set([c.position for c in self.carts]))
			if numberOfPositions < numberOfCarts:
				print("Collision at {}".format(cart.position))
				self.removeCartsAt(cart.position)
			else:
				cart.turn(self.grid[cart.position])

	def removeCartsAt(self, collisionPosition):
		self.carts = [cart for cart in self.carts if cart.position != collisionPosition]

#############
# Functions #
#############
def getTrackSystemFromFile(fileName):
	trackSystem = TrackSystem()
	with open(fileName) as f:
		lines = f.readlines()
		for y in range(len(lines)):
			line = lines[y].rstrip()
			for x in range(len(line)):
				char = line[x]
				if char != " ":
					trackSystem.addTrackAndOrCart(x, y, char)
	return trackSystem

def printTrackSystem(trackSystem):
	maxX = max([position[0] for position in trackSystem.grid])
	maxY = max([position[1] for position in trackSystem.grid])
	for y in range(maxY+1):
		line = ""
		for x in range(maxX+1):
			cartsHere = [cart for cart in trackSystem.carts if cart.position == (x,y)]
			if cartsHere:
				line += Cart.directionToSymbol[cartsHere[0].direction]
			elif (x,y) in trackSystem.grid:
				line += Direction.getSymbol(trackSystem.grid[(x,y)])
			else:
				line += " "
		print(line)

########
# Main #
########
trackSystem = getTrackSystemFromFile("input13.txt")
while len(trackSystem.carts) > 1:
	trackSystem.tick()
print("Last cart remaining is at {}".format(trackSystem.carts[0].position))
