from aoclib.direction import Direction
from aoclib.filereader import getFileAsSingleString
from dec20.facility import Facility

########
# Main #
########
if __name__ == "__main__":
	regex = getFileAsSingleString("input20.txt").lstrip("^").rstrip().rstrip("$")
	facility = Facility()
	facility.exploreFacilityAccordingToRegex(regex)
	roomToDistance = facility.getShortestDistanceToEveryRoom()
	
	# Part 1
	maxDistance = max(x for x in roomToDistance.values())
	print("Shortest distance to most distant room: {}".format(maxDistance))
	# Part 2
	numberOfRooms = len([x for x in roomToDistance.values() if x >= 1000])
	print("Number of rooms requiring passing through at least 1000 doors: {}".format(numberOfRooms))
