from aoclib.filereader import getFileAsListOfString
from dec13.direction import Direction
from dec13.track import TrackSystem, Cart

class Parser:
	cartSymbolToDirection = {
		"<": Direction.left,
		">": Direction.right,
		"^": Direction.up,
		"v": Direction.down
	}
	cartDirectionToSymbol = {v: k for (k, v) in cartSymbolToDirection.items()}

	def getTrackSystemFromFile(self, fileName):
		trackSystem = TrackSystem()
		lines = getFileAsListOfString(fileName)
		for y in range(len(lines)):
			line = lines[y].rstrip()
			for x in range(len(line)):
				symbol = line[x]
				if symbol != " ":
					self._addTrackAndOrCart(trackSystem, x, y, symbol)
		return trackSystem
	
	def printTrackSystem(self, trackSystem):
		maxX = max([position[0] for position in trackSystem.grid])
		maxY = max([position[1] for position in trackSystem.grid])
		for y in range(maxY+1):
			line = ""
			for x in range(maxX+1):
				cart = next((cart for cart in trackSystem.carts if cart.position == (x,y)), None)
				if cart is not None:
					line += Parser.cartDirectionToSymbol[cart.direction]
				elif (x,y) in trackSystem.grid:
					line += self._getSymbolFromDirections(trackSystem.grid[(x,y)])
				else:
					line += " "
			print(line)
	
	def _addTrackAndOrCart(self, trackSystem, x, y, symbol):
		pos = (x,y)
		posLeft = (x-1,y)
		directions = set()
		if symbol == "+":
			directions |= Direction.all
		elif symbol == "-":
			directions |= Direction.horizontal
		elif symbol == "|":
			directions |= Direction.vertical
		elif symbol == "/":
			if posLeft in trackSystem.grid and Direction.right in trackSystem.grid[posLeft]:
				directions |= {Direction.left, Direction.up}
			else:
				directions |= {Direction.right, Direction.down}
		elif symbol == "\\":
			if posLeft in trackSystem.grid and Direction.right in trackSystem.grid[posLeft]:
				directions |= {Direction.left, Direction.down}
			else:
				directions |= {Direction.right, Direction.up}
		else:
			cart = Cart(pos, Parser.cartSymbolToDirection[symbol])
			trackSystem.addCart(cart)
			directions |= {cart.direction, Direction.getOppositeDirection(cart.direction)}
		trackSystem.addTrack(pos, directions)
	
	def _getSymbolFromDirections(self, directions):
		if directions == Direction.all:
			return "+"
		elif directions == Direction.horizontal:
			return "-"
		elif directions == Direction.vertical:
			return "|"
		elif directions == {Direction.left, Direction.up} \
				or directions == {Direction.right, Direction.down}:
			return "/"
		elif directions == {Direction.left, Direction.down} \
				or directions == {Direction.right, Direction.up}:
			return "\\"
		else:
			raise ValueError("Unknown track section. Directions: {}".format(directions))
