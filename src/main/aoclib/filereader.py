def getFileAsSingleString(fileName):
	with open(fileName) as f:
		return f.read()

def getFileAsListOfString(fileName):
	with open(fileName) as f:
		return f.readlines()
