from aoclib.sortedlist import SortedList

class AStar:
	"""
	A* search.
	Search nodes must implement:
	- isSolution()         Returns True iff the node is a solution.
	- getSuccessorNodes()  Returns a list of nodes.
	- __le__, __ne__       For sorting
	- getState()           To determine whether a node represents a state
	                       that has already been evaluated
	"""
	
	def __init__(self, initialNodes, *, ascending=True):
		self.nodeList = SortedList(ascending=ascending)
		for node in initialNodes:
			self.nodeList.insert(node)

	def findBestSolutions(self):
		nCreated = self.nodeList.getSize()
		evaluatedNodes = set()
		nSkipped = 0
		solutionNodes = []
		while not self.nodeList.isEmpty():
			node = self.nodeList.pop()
			if node.getState() in evaluatedNodes:
				nSkipped += 1
				continue
			else:
				evaluatedNodes.add(node.getState())
			if len(solutionNodes) > 0 and node != solutionNodes[0]:
				break
			if node.isSolution():
				solutionNodes.append(node)
			for successorNode in node.getSuccessorNodes():
				nCreated += 1
				self.nodeList.insert(successorNode)
		stats = SearchStats(created=nCreated, evaluated=len(evaluatedNodes), skipped=nSkipped)
		return (solutionNodes, stats)

class SearchStats:
	def __init__(self, created=0, evaluated=0, skipped=0):
		self.created = created
		self.evaluated = evaluated
		self.skipped = skipped
