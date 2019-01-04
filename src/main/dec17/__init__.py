from dec17.parser import getWorldFromFile
from dec17.world import World

if __name__ == "__main__":
	world = getWorldFromFile("input17.txt")
	world.letWaterFlow()
	allWaterPositions = world.waterSettled | world.waterPassed
	part1Answer = len([1 for (x,y) in allWaterPositions if y >= world.minY and y <= world.maxY])
	print("Part 1. Number of squares with water: {}".format(part1Answer))
	part2Answer = len([1 for (x,y) in world.waterSettled if y >= world.minY and y <= world.maxY])
	print("Part 2. Number of squares with settled water: {}".format(part2Answer))
