import unittest

from dec20.regex import getRegexWithinParentheses, splitRegexOnBranches

class TestSuite(unittest.TestCase):
	def test_getRegexWithinParentheses(self):
		regexList = [
			("(SW)EEE", "SW", "EEE"),
			("(SW(|WW))EW(S|W)", "SW(|WW)", "EW(S|W)"),
		]
		for (regex, expectedRegexWithinParentheses, expectedRegexTail) in regexList:
			message = "Regex: {}".format(regex)
			(regexWithinParentheses, regexRemaining) = getRegexWithinParentheses(regex)
			self.assertEqual(regexWithinParentheses, expectedRegexWithinParentheses, message)
			self.assertEqual(regexRemaining, expectedRegexTail, message)

	def test_splitRegexOnBranches(self):
		testdata = [
			("NSEWWW(NSW(|EE))E", ["NSEWWW(NSW(|EE))E"]),
			("|NS(W|E)NN|E(|WWW)S|NW|", ["", "NS(W|E)NN", "E(|WWW)S", "NW", ""])
		]
		for (regex, expectedRegexList) in testdata:
			regexList = splitRegexOnBranches(regex)
			self.assertEqual(regexList, expectedRegexList)
