from dec13.track import TrackSystem

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
