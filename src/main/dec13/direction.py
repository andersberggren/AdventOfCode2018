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
