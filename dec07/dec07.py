import re

###########
# Classes #
###########
class Step:
	def __init__(self, id):
		self.id = id
		# timeLeft is only used in part 2
		self.timeLeft = 61 + ord(id) - ord('A')
		self.isCompleted = False
		self.dependees = set()

	# Adds a dependee, i.e. a Step that has to be completed before this Step can be completed.
	def addDependee(self, dependee):
		self.dependees.add(dependee)

	def doOneSecondOfWork(self):
		self.timeLeft -= 1
		if self.timeLeft == 0:
			self.isCompleted = True

	# Returns True iff all dependees are already completed.
	def canBeWorkedOn(self):
		return all(x.isCompleted for x in self.dependees)

#############
# Functions #
#############
# Reads a file and returns a list of Steps (with dependencies to other Steps).
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

def getStepsThatCanBeWorkedOn(steps):
	return [step for step in steps if step.canBeWorkedOn() and not step.isCompleted]

def findCompletionOrderPart1(steps):
	solution = ""
	while not all([step.isCompleted for step in steps]):
		nextStep = sorted(getStepsThatCanBeWorkedOn(steps), key=lambda step: step.id)[0]
		solution += nextStep.id
		nextStep.isCompleted = True
	return solution

def findCompletionTimePart2(steps, numberOfWorkers):
	timeSpent = 0
	while not all([step.isCompleted for step in steps]):
		candidateSteps = getStepsThatCanBeWorkedOn(steps)
		for i in range(min(len(candidateSteps), numberOfWorkers)):
			step = candidateSteps[i]
			step.doOneSecondOfWork()
		timeSpent += 1
	return timeSpent

########
# Main #
########
# Part 1
steps = getStepsFromFile("input07")
solution = findCompletionOrderPart1(steps)
print("Part 1: Complete the steps in this order: {}".format(solution))

# Part 2
steps = getStepsFromFile("input07")
time = findCompletionTimePart2(steps, 5)
print("Part 2: Takes {} seconds to complete".format(time))
