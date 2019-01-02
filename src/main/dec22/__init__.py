import re

from aoclib.filereader import getFileAsListOfString
from aoclib.search import AStar
from dec22.cave import Cave
from dec22.searchnode import SearchNode

#############
# Functions #
#############
# Returns (depth, targetLocation)
def getDepthAndTargetLocationFromFile(fileName):
	for line in getFileAsListOfString(fileName):
		depthMatch = re.match("^depth: (\d+)$", line)
		targetMatch = re.match("^target: (\d+),(\d+)", line)
		if depthMatch:
			depth = int(depthMatch.group(1))
		elif targetMatch:
			target = (int(targetMatch.group(1)), int(targetMatch.group(2)))
	return (depth, target)

########
# Main #
########
if __name__ == "__main__":
	(depth, targetLocation) = getDepthAndTargetLocationFromFile("input22.txt")
	cave = Cave(depth, targetLocation)
	
	# Part 1
	print("Total risk: {}".format(cave.getTotalRisk()))
	
	# Part 2
	initialNode = SearchNode(None, cave, (0,0))
	aStar = AStar([initialNode], ascending=True, debugInterval=10000)
	(solutionNode, stats) = aStar.findBestSolution()
	print("Solution found. Time to reach target: {}".format(solutionNode.timeSpent))
