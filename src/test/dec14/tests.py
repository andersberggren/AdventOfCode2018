import unittest

from dec14 import dec14

class TestSuite(unittest.TestCase):
	def test_ChocolateLaboratory(self):
		elvesAndScores = [
			([0, 1], [3, 7]),
			([0, 1], [1, 0]),
			([4, 3], [1, 0]),
			([6, 4], [1]),
			([0, 6], [2]),
			([4, 8], [4]),
			([6, 3], [5]),
		]
		expectedScores = []
		lab = None
		for (elves, scores) in elvesAndScores:
			expectedElves = elves
			expectedScores.extend(scores)
			if lab is None:
				lab = dec14.ChocolateLaboratory()
			else:
				lab.update()
			self.assertEqual(lab.recipeScores, expectedScores)
			self.assertEqual(lab.elves, expectedElves)

	def test_part1(self):
		lab = dec14.ChocolateLaboratory()
		recipesAndAnswers = [
			(   5, "0124515891"),
			(   9, "5158916779"),
			(  18, "9251071085"),
			(2018, "5941429882")
		]
		answerSize = 10
		for (numberOfRecipes, expectedAnswer) in recipesAndAnswers:
			actualAnswer = dec14.part1(lab, numberOfRecipes, answerSize)
			self.assertEqual(actualAnswer, expectedAnswer)

	def test_part2(self):
		lab = dec14.ChocolateLaboratory()
		digitSequencesAndAnswers = [
			("0124515891",    5),
			("5158916779",    9),
			("9251071085",   18),
			("5941429882", 2018)
		]
		for (digitSequenceAsString, expectedAnswer) in digitSequencesAndAnswers:
			digitSequence = [int(x) for x in digitSequenceAsString]
			actualAnswer = dec14.part2(lab, digitSequence)
			self.assertEqual(actualAnswer, expectedAnswer)

	def test_matchSubList(self):
		testDataMatch = [
			([1, 3, 3, 7],    [3, 3], 1),
			([1, 7, 6, 7, 6], [],     0),
			([5, 5, 0, 1, 4], [1, 4], 3)
		]
		testDataNoMatch = [
			([1, 3, 3, 7],    [1, 4],    0),
			([1, 7, 6, 7, 6], [7],       4),
			([5, 5, 0, 1, 4], [5, 0, 4], 1)
		]
		for (fullList, subList, offset) in testDataMatch:
			self.assertTrue(dec14.matchSubList(fullList, subList, offset))
		for (fullList, subList, offset) in testDataNoMatch:
			self.assertFalse(dec14.matchSubList(fullList, subList, offset))
