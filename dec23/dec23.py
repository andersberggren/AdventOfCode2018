import re

from aoclib.distance import getManhattanDistance3

###########
# Classes #
###########
class Nanobot:
	def __init__(self, pos, radius):
		self.pos = pos
		self.radius = radius

#############
# Functions #
#############
def getNanobotsFromFile(fileName):
	with open(fileName) as f:
		return [getNanobotFromString(x) for x in f.readlines()]

def getNanobotFromString(s):
	match = re.match("pos=<([0-9,-]+)>, r=(\d+)", s)
	pos = tuple([int(x) for x in match.group(1).split(",")])
	radius = int(match.group(2))
	return Nanobot(pos, radius)

########
# Main #
########
nanobots = getNanobotsFromFile("input23.txt")
strongestNanobot = sorted(nanobots, key=lambda x: x.radius, reverse=True)[0]
part1 = len([x for x in nanobots if getManhattanDistance3(x.pos, strongestNanobot.pos) <= strongestNanobot.radius])
print("Part 1: {} nanobots are in range".format(part1))
