###########
# Classes #
###########
class Cart:
	def __init__(self, startPosition, startDirection):
		self.position = startPosition
		self.direction = startDirection
		self.futureTurns = [self.turnLeft, self.turnNot, self.turnRight]

	def move(self):
		oldPosition = self.position
		self.position = (self.position[0]+self.direction[0], self.position[1]+self.direction[1])

	def turn(self, directions):
		if isIntersection(directions):
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
		self.direction = (self.direction[1], -self.direction[0])

	def turnRight(self):
		self.direction = (-self.direction[1], self.direction[0])

	def turnNot(self):
		pass

	def __repr__(self):
		return "Cart[position={p},direction={d}]".format(p=self.position, d=self.direction)

	def __cmp__(self, other):
		if self.direction[1] < other.direction[1]:
			return -1
		elif self.direction[1] > other.direction[1]:
			return 1
		else:
			return self.direction[0] - other.direction[0]

	@staticmethod
	def createFromString(startPosition, s):
		if s == "<":
			return Cart(startPosition, Direction.left)
		elif s == ">":
			return Cart(startPosition, Direction.right)
		elif s == "^":
			return Cart(startPosition, Direction.up)
		elif s == "v":
			return Cart(startPosition, Direction.down)
		else:
			raise ValueError("Invalid cart: {}".format(s))

	@staticmethod
	def cartSort(cart):
		return (cart.position[1], cart.position[0])

class Direction:
	@staticmethod
	def getDirectionToTheLeft(direction):
		return (direction[1], -direction[0])

	@staticmethod
	def getDirectionToTheRight(direction):
		return (-direction[1], direction[0])

Direction.left  = (-1,  0)
Direction.right = ( 1,  0)
Direction.up    = ( 0, -1)
Direction.down  = ( 0,  1)
Direction.all = [Direction.left, Direction.right, Direction.up, Direction.down]
Direction.horizontal = [Direction.left, Direction.right]
Direction.vertical = [Direction.up, Direction.down]

class TrackSystem:
	def __init__(self):
		self.grid = {}
		self.carts = []

	def addTrackAndOrCart(self, x, y, type):
		position = (x,y)
		positionToTheLeft = (x-1,y)
		directions = set()
		if type == "|":
			directions.add(Direction.up)
			directions.add(Direction.down)
		elif type == "-":
			directions.add(Direction.left)
			directions.add(Direction.right)
		elif type == "/":
			if positionToTheLeft in self.grid and Direction.right in self.grid[positionToTheLeft]:
				directions.add(Direction.left)
				directions.add(Direction.up)
			else:
				directions.add(Direction.right)
				directions.add(Direction.down)
		elif type == "\\":
			if positionToTheLeft in self.grid and Direction.right in self.grid[positionToTheLeft]:
				directions.add(Direction.left)
				directions.add(Direction.down)
			else:
				directions.add(Direction.right)
				directions.add(Direction.up)
		elif type == "+":
			directions.add(Direction.left)
			directions.add(Direction.right)
			directions.add(Direction.up)
			directions.add(Direction.down)
		elif any([type == cartChar for cartChar in ["<", ">", "^", "v"]]):
			cart = Cart.createFromString(position, type)
			self.carts.append(cart)
			directions.add(cart.direction)
			directions.add((-cart.direction[0], -cart.direction[1]))
		else:
			raise ValueError("Invalid track symbol at ({},{}): {}".format(x, y, type))
		self.grid[(x,y)] = directions

	# Move all carts one step.
	def tick(self):
		hasCollided = False
		for cart in sorted(self.carts, key=Cart.cartSort):
			cart.move()
			if len(set([c.position for c in self.carts])) != len(self.carts):
				hasCollided = True
				print("Collision at {}".format(cart.position))
				self.removeCartsAt(cart.position)
			else:
				cart.turn(self.grid[cart.position])
		return hasCollided

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

def isIntersection(directions):
	return all([d in directions for d in Direction.all])

def printTrackSystem(trackSystem):
	maxX = max([coord[0] for coord in trackSystem.grid])
	maxY = max([coord[1] for coord in trackSystem.grid])
	for y in range(maxY+1):
		line = ""
		for x in range(maxX+1):
			if (x,y) in [cart.position for cart in trackSystem.carts]:
				line += "C"
			elif (x,y) in trackSystem.grid:
				directions = trackSystem.grid[(x,y)]
				if all([d in directions for d in Direction.all]):
					line += "+"
				elif all([d in directions for d in Direction.horizontal]):
					line += "-"
				elif all([d in directions for d in Direction.vertical]):
					line += "|"
				elif all([d in directions for d in [Direction.left, Direction.up]]) \
						or all([d in directions for d in [Direction.right, Direction.down]]):
					line += "/"
				elif all([d in directions for d in [Direction.left, Direction.down]]) \
						or all([d in directions for d in [Direction.right, Direction.up]]):
					line += "\\"
				else:
					raise ValueError("Unknown track at ({x},{y}), Directions: {dir}".format(
							x=x, y=y, dir=directions))
			else:
				line += " "
		print(line)

########
# Main #
########
trackSystem = getTrackSystemFromFile("input13")
printTrackSystem(trackSystem)

while len(trackSystem.carts) > 1:
	trackSystem.tick()
print("Last cart remaining is at {}".format(trackSystem.carts[0].position))
