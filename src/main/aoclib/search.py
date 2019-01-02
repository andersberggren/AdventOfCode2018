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
	
	def __init__(self, initialNodes, *, ascending=True, debugInterval=None):
		self.nodeList = SortedList(ascending=ascending)
		for node in initialNodes:
			self.nodeList.insert(node)
		self.debugInterval = debugInterval
	
	def findBestSolution(self):
		(solutionNodes, stats) = self._findBestSolutions(allowMultiple=False)
		solutionNode = solutionNodes[0] if len(solutionNodes) > 0 else None
		return (solutionNode, stats)
	
	def findBestSolutions(self):
		return self._findBestSolutions(allowMultiple=True)
	
	def _findBestSolutions(self, allowMultiple=True):
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
				if not allowMultiple:
					break
			for successorNode in node.getSuccessorNodes():
				nCreated += 1
				if successorNode.getState() in evaluatedNodes:
					nSkipped += 1
				else:
					self.nodeList.insert(successorNode)
				if self.debugInterval is not None and nCreated % self.debugInterval == 0:
					print("Created: {c:,}  Evaluated: {e:,}  Skipped: {s:,}  In list: {l:,}".format(
						c=nCreated, l=self.nodeList.getSize(), e=len(evaluatedNodes), s=nSkipped))
					print("Current node is {}".format(node))
		stats = SearchStats(created=nCreated, evaluated=len(evaluatedNodes), skipped=nSkipped)
		return (solutionNodes, stats)

class SearchStats:
	def __init__(self, created=0, evaluated=0, skipped=0):
		self.created = created
		self.evaluated = evaluated
		self.skipped = skipped
