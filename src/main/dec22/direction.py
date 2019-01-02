class Direction:
	up    = ( 0, -1)
	down  = ( 0,  1)
	left  = (-1,  0)
	right = ( 1,  0)
	all = [up, down, left, right]
	
	@staticmethod
	def getNewLocation(location, direction):
		return (location[0]+direction[0], location[1]+direction[1])
