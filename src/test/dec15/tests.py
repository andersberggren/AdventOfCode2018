import unittest

from dec15 import Creature
from dec15.world import World, UnreachableError

class TestSuite(unittest.TestCase):
	# ######
	# #E#E##
	# #G E #
	# # G# #
	# ## # #
	# #    #
	# ######
	def setUp(self):
		self.openPositions = [
			(1,1), (3,1),
			(1,2), (2,2), (3,2), (4,2),
			(1,3), (2,3), (4,3),
			(2,4), (4,4),
			(1,5), (2,5), (3,5), (4,5)
		]
		self.creatures = [
			Creature(self.openPositions[4], "Elf"),
			Creature(self.openPositions[0], "Elf"),
			Creature(self.openPositions[1], "Elf"),
			Creature(self.openPositions[7], "Goblin"),
			Creature(self.openPositions[2], "Goblin")
		]
		self.world = World()
		for position in self.openPositions:
			self.world.addPosition(position)
		for creature in self.creatures:
			self.world.addCreature(creature)

	def test_creature(self):
		position = (3,7)
		creatureType = "Elf"
		creature = Creature(position, creatureType)
		self.assertEqual(creature.position, position)
		self.assertEqual(creature.type, creatureType)

	def test_world(self):
		self.assertEqual(len(self.world.allPositions), len(self.openPositions))
		for position in self.openPositions:
			self.assertTrue(position in self.world.allPositions)
		self.assertEqual(len(self.world.positionToCreature), len(self.creatures))
		for expectedCreature in self.creatures:
			actualCreature = self.world.positionToCreature[expectedCreature.position]
			self.assertIs(actualCreature, expectedCreature)

	def test_world_getCreaturesSortedByExecutionOrder(self):
		actualCreatures = self.world.getCreaturesSortedByExecutionOrder()
		self.assertEqual(len(actualCreatures), len(self.creatures))
		self.assertIs(actualCreatures[0], self.creatures[1])
		self.assertIs(actualCreatures[1], self.creatures[2])
		self.assertIs(actualCreatures[2], self.creatures[4])
		self.assertIs(actualCreatures[3], self.creatures[0])
		self.assertIs(actualCreatures[4], self.creatures[3])

	def test_world_getEnemies(self):
		actualEnemies = self.world.getEnemies(self.creatures[0].type)
		self.assertEqual(len(actualEnemies), 2)
		self.assertTrue(self.creatures[3] in actualEnemies)
		self.assertTrue(self.creatures[4] in actualEnemies)
		actualEnemies = self.world.getEnemies(self.creatures[4].type)
		self.assertEqual(len(actualEnemies), 3)
		self.assertTrue(self.creatures[0] in actualEnemies)
		self.assertTrue(self.creatures[1] in actualEnemies)
		self.assertTrue(self.creatures[2] in actualEnemies)

	def test_world_getAdjacentSquares(self):
		adjacentSquares = self.world.getAdjacentSquares((1,2))
		self.assertEqual(len(adjacentSquares), 3)
		self.assertTrue((1,1) in adjacentSquares)
		self.assertTrue((1,3) in adjacentSquares)
		self.assertTrue((2,2) in adjacentSquares)

	def test_world_getAdjacentEmptySquares(self):
		squares = self.world.getAdjacentEmptySquares((1,2))
		self.assertEqual(len(squares), 2)
		self.assertTrue((1,3) in squares)
		self.assertTrue((2,2) in squares)

	def test_world_getDistance(self):
		self.assertEqual(self.world.getDistance((1,2), (2,2)), 1)
		self.assertEqual(self.world.getDistance((2,3), (4,2)), 7)
		self.assertEqual(self.world.getDistance((3,2), (3,5)), 5)
		try:
			self.world.getDistance((3,2), (1,3))
			self.fail("Expected UnreachableError")
		except UnreachableError:
			pass

	def test_world_isCombatOver(self):
		self.assertFalse(self.world.isCombatOver())
		for creature in list(self.world.positionToCreature.values()):
			if creature.type == "Goblin":
				del self.world.positionToCreature[creature.position]
		self.assertTrue(self.world.isCombatOver())

	def test_world_isEmpty(self):
		self.assertTrue(self.world.isEmpty((2,2)))
		self.assertTrue(self.world.isEmpty((4,2)))
		self.assertTrue(self.world.isEmpty((4,3)))
		self.assertFalse(self.world.isEmpty((0,0)))
		self.assertFalse(self.world.isEmpty((1,1)))
		self.assertFalse(self.world.isEmpty((1,2)))
		self.assertFalse(self.world.isEmpty((100,100)))

	def test_world_isReachable(self):
		self.assertTrue(self.world.isReachable((1,2), (2,2)))
		self.assertTrue(self.world.isReachable((2,3), (4,4)))
		self.assertFalse(self.world.isReachable((1,2), (2,3)))
		self.assertFalse(self.world.isReachable((1,2), (4,4)))

	def test_world_existsAdjacentEnemy(self):
		self.assertFalse(self.world.existsAdjacentEnemy(self.creatures[0]))
		self.assertTrue(self.world.existsAdjacentEnemy(self.creatures[4]))
