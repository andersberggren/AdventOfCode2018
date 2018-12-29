def getFileAsSingleString(fileName):
	with open(fileName) as f:
		return f.read()
