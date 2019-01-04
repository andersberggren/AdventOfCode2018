from dec13.direction import Direction
from dec13.parser import getTrackSystemFromFile
from dec13.track import TrackSystem, Cart

#############
# Functions #
#############
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
if __name__ == "__main__":
	trackSystem = getTrackSystemFromFile("input13.txt")
	while len(trackSystem.carts) > 1:
		trackSystem.tick()
		printTrackSystem(trackSystem)
	print("Last cart remaining is at {}".format(trackSystem.carts[0].position))
