class Direction:
	left  = (-1,  0)
	right = ( 1,  0)
	up    = ( 0, -1)
	down  = ( 0,  1)
	all = {left, right, up, down}
	horizontal = {left, right}
	vertical = {up, down}

	@staticmethod
	def getOppositeDirection(direction):
		return (-direction[0], -direction[1])

	@staticmethod
	def getDirectionToTheLeft(direction):
		return (direction[1], -direction[0])

	@staticmethod
	def getDirectionToTheRight(direction):
		return (-direction[1], direction[0])
