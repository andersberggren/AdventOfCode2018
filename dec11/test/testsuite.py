import unittest
from dec11 import dec11

class TestSuite(unittest.TestCase):
	# Test data for power level of a single cell:
	# (serialNumber, (x,y), expectedPowerLevel)
	powerLevelTestData = [
			(8,  (  3,  5),  4),
			(57, (122, 79), -5),
			(39, (217,196),  0),
			(71, (101,153),  4)
			]

	def test_getLargestDivisorLargerThanSelf(self):
		testData = [
				( 1,  1),
				( 2,  1),
				( 3,  1),
				( 4,  2),
				( 5,  1),
				( 6,  3),
				( 7,  1),
				( 8,  4),
				( 9,  3),
				(10,  5),
				(13,  1),
				(81, 27)
				]
		for (input, expectedDivisor) in testData:
			self.assertEqual(dec11.getLargestDivisorSmallerThanSelf(input), expectedDivisor)

	def test_calcPowerLevelForSingleCell(self):
		for (serialNumber, (x,y), expectedPowerLevel) in self.powerLevelTestData:
			size = max([x, y])
			grid = dec11.Grid(size, serialNumber)
			self.assertEqual(grid.calcPowerLevelForSingleCell(x, y), expectedPowerLevel,
					"Serial number {sn}, coordinate ({x},{y})".format(sn=serialNumber, x=x, y=y))

	def test_calcTotalPowerInSquare(self):
		for (serialNumber, (x,y), expectedPowerLevel) in self.powerLevelTestData:
			size = max([x, y])
			grid = dec11.Grid(size, serialNumber)
			self.assertEqual(grid.calcTotalPowerInSquare(x, y, 1), expectedPowerLevel,
					"Serial number {sn}, coordinate ({x},{y})".format(sn=serialNumber, x=x, y=y))
