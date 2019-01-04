def getRegexWithinParentheses(regex):
	""" Returns (regexWithinParentheses, regexTail). """
	if regex[0] != "(":
		raise RuntimeError("Expected regex to start with \"(\", but was \"{}\"".format(regex[0]))
	# "balance" is number of "(" minus number of ")"
	balance = 1
	i = 1
	while balance > 0:
		if regex[i] == "(":
			balance += 1
		elif regex[i] == ")":
			balance -= 1
		i += 1
	regexWithinParentheses = regex[1:i-1]
	regexTail = regex[i:]
	return (regexWithinParentheses, regexTail)

def splitRegexOnBranches(regex):
	""" Splits regex on "|", and returns a list of regex. """
	regexList = []
	balance = 0
	i = 0
	while i < len(regex):
		if regex[i] == "|" and balance == 0:
			regexList.append(regex[:i])
			regex = regex[i+1:]
			i = 0
		else:
			if regex[i] == "(":
				balance += 1
			elif regex[i] == ")":
				balance -= 1
			i += 1
	regexList.append(regex)
	return regexList
