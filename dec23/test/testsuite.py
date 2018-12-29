import unittest

import dec23

class Test(unittest.TestCase):
	def test_getManhattanDistanceFromBoxToPoint(self):
		boxPos = (3, -2, -4)
		boxSize = (1, 3, 7)
		pos = (4, -3, 4)
		self.assertEqual(dec23.getManhattanDistance3FromCuboid(boxPos, boxSize, pos), 4)
		pos = (-3, 1, -6)
		self.assertEqual(dec23.getManhattanDistance3FromCuboid(boxPos, boxSize, pos), 9)
		pos = (1, -1, 1)
		self.assertEqual(dec23.getManhattanDistance3FromCuboid(boxPos, boxSize, pos), 2)
	
	def test_getBoundingBox(self):
		nanobots = [
			dec23.Nanobot((11, 0,-3), 1),
			dec23.Nanobot(( 4, 1,14), 1),
			dec23.Nanobot((-2,13, 0), 1),
			dec23.Nanobot((17, 9,-7), 1),
		]
		self.assertEqual(dec23.getBoundingBox(nanobots), ((-2,0,-7), (20,14,22)))
