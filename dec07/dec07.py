import re

###########
# Classes #
###########
class Step:
	def __init__(self, id):
		self.id = id
		self.isCompleted = False
		self.dependees = set()

	# Adds a dependee, i.e. a Step that has to be completed before this Step can be completed.
	def addDependee(self, dependee):
		self.dependees.add(dependee)

	# Returns True iff all dependees are already completed.
	def canBeCompleted(self):
		return all(x.isCompleted for x in self.dependees)

	def toString(self):
		s = "Step[id={id},dependees={dependees}]"
		return s.format(id=self.id, dependees="".join([x.id for x in self.dependees]))

#############
# Functions #
#############
# Reads a file and returns a Steps (with dependencies to other Steps).
def getStepsFromFile(fileName):
	# Map from ID to Step
	steps = {}
	with open(fileName) as f:
		for line in f.readlines():
			m = re.match("Step (.) must be finished before step (.) can begin.$", line)
			if m:
				idDependant = m.group(2)
				idDependee =  m.group(1)
				for id in [idDependant, idDependee]:
					if id not in steps:
						steps[id] = Step(id)
				steps[idDependant].addDependee(steps[idDependee])
			else:
				raise RuntimeError("Line in file has incorrect format: {}".format(line))
	return steps.values()

########
# Main #
########
steps = getStepsFromFile("input07")
#[print(step.toString()) for step in steps]

solution = ""
while not all([step.isCompleted for step in steps]):
	candidateSteps = [step for step in steps if step.canBeCompleted() and not step.isCompleted]
	nextStep = sorted(candidateSteps, key=lambda step: step.id)[0]
	solution += nextStep.id
	nextStep.isCompleted = True
print("Complete the steps in this order: {}".format(solution))
