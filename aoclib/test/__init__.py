import unittest

from ..geometry import getBoundingBox, getManhattanDistance3FromBox

class Test(unittest.TestCase):
    def test_getManhattanDistance3FromBox(self):
        boxPos = (3, -2, -4)
        boxSize = (1, 3, 7)
        pos = (4, -3, 4)
        self.assertEqual(getManhattanDistance3FromBox(boxPos, boxSize, pos), 4)
        pos = (-3, 1, -6)
        self.assertEqual(getManhattanDistance3FromBox(boxPos, boxSize, pos), 9)
        pos = (1, -1, 1)
        self.assertEqual(getManhattanDistance3FromBox(boxPos, boxSize, pos), 2)
    
    def test_getBoundingBox(self):
        points = [
            (11, 0,-3),
            ( 4, 1,14),
            (-2,13, 0),
            (17, 9,-7)
        ]
        self.assertEqual(getBoundingBox(points), ((-2,0,-7), (20,14,22)))
