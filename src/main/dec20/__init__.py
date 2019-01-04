from aoclib.direction import Direction
from aoclib.filereader import getFileAsSingleString
from dec20.facility import Facility
from dec20.regex import getRegexWithinParentheses, splitRegexOnBranches

#############
# Functions #
#############
# Arguments:
#   facility   The facility to explore.
#   regex      Remaining regex.
#   positions  A set of positions, where we are currently at.
# Returns a set of positions, where we are at after exploring the regex.
def exploreFacilityAccordingToRegex(facility, regex, positions):
	if len(regex) == 0:
		return positions
	regexList = splitRegexOnBranches(regex)
	if len(regexList) > 1:
		# Recursive call for each branch
		newPositions = set()
		for regexSection in regexList:
			newPositions |= exploreFacilityAccordingToRegex(facility, regexSection, positions)
		return newPositions
	else:
		# Single branch
		if regex[0] == "(":
			(regexWithinParentheses, regexTail) = getRegexWithinParentheses(regex)
			positions = exploreFacilityAccordingToRegex(facility, regexWithinParentheses, positions)
			return exploreFacilityAccordingToRegex(facility, regexTail, positions)
		else:
			# Evaluate one symbol at a time, until "("
			for i in range(len(regex)):
				symbol = regex[i]
				if symbol in Facility.symbolToDirection:
					direction = Facility.symbolToDirection[symbol]
					newPositions = set()
					for position in positions:
						facility.addDoor(position, direction)
						newPositions.add(Direction.getNewLocation(position, direction))
					positions = newPositions
				elif symbol == "(":
					return exploreFacilityAccordingToRegex(facility, regex[i:], positions)
				else:
					raise RuntimeError("Unexpected symbol: {}".format(symbol))
			return positions

########
# Main #
########
if __name__ == "__main__":
	facility = Facility()
	regex = getFileAsSingleString("input20.txt").lstrip("^").rstrip().rstrip("$")
	positions = {(0,0)}
	exploreFacilityAccordingToRegex(facility, regex, positions)
	roomToDistance = facility.getShortestDistanceToEveryRoom()
	# Part 1
	maxDistance = max(x for x in roomToDistance.values())
	print("Shortest distance to most distant room: {}".format(maxDistance))
	# Part 2
	numberOfRooms = len([x for x in roomToDistance.values() if x >= 1000])
	print("Number of rooms requiring passing through at least 1000 doors: {}".format(numberOfRooms))
