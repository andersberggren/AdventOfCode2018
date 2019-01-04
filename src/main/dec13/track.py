from dec13.direction import Direction

class TrackSystem:
	def __init__(self):
		self.grid = {}
		self.carts = []
	
	def addTrack(self, position, directions):
		self.grid[position] = directions
	
	def addCart(self, cart):
		self.carts.append(cart)
	
	# Moves all carts one step.
	def tick(self):
		for cart in sorted(self.carts):
			cart.move()
			numberOfCarts = len(self.carts)
			numberOfPositions = len(set([c.position for c in self.carts]))
			if numberOfPositions < numberOfCarts:
				print("Collision at {}".format(cart.position))
				# Remove carts at collision position
				self.carts = [x for x in self.carts if x.position != cart.position]
			else:
				cart.turn(self.grid[cart.position])

class Cart:
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
		isIntersection = all(d in directions for d in Direction.all)
		if isIntersection:
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
