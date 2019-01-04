import re

from aoclib.filereader import getFileAsListOfString
from dec17.world import World

def getWorldFromFile(fileName):
	world = World()
	for line in getFileAsListOfString(fileName):
		(x, y, width, height) = stringToRectangle(line)
		world.addClay(x, y, width, height)
	return world

def stringToRectangle(s):
	""" Reads a string and returns (x, y, width, height). """
	xMatch = re.search("x=(\d+)(..(\d+))?", s)
	yMatch = re.search("y=(\d+)(..(\d+))?", s)
	x = int(xMatch.group(1))
	if xMatch.group(3) is None:
		width = 1
	else:
		width = int(xMatch.group(3)) + 1 - x
	y = int(yMatch.group(1))
	if yMatch.group(3) is None:
		height = 1
	else:
		height = int(yMatch.group(3)) + 1 - y
	return (x, y, width, height)

def printWorld(world):
	minX = min([pos[0] for pos in world.clay])
	maxX = max([pos[0] for pos in world.clay])
	maxY = max([pos[1] for pos in world.clay])
	for y in range(maxY+1):
		for x in range(minX, maxX+1):
			position = (x,y)
			symbol = " "
			if position in world.clay:
				symbol = "#"
			elif position == world.waterSpring:
				symbol = "+"
			elif position in world.waterSettled:
				symbol = "~"
			elif position in world.waterPassed:
				symbol = "|"
			print(symbol, end="")
		print()
