from aoclib.direction import Direction
from dec13.parser import Parser
from dec13.track import TrackSystem, Cart

if __name__ == "__main__":
	trackSystem = Parser().getTrackSystemFromFile("input13.txt")
	while len(trackSystem.carts) > 1:
		trackSystem.tick()
	print("Last cart remaining is at {}".format(trackSystem.carts[0].position))
