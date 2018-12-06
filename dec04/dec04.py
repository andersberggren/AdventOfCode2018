import re

###########
# Classes #
###########
class Guard:
	def __init__(self, id):
		self.id = int(id)
		self.minutesAsleep = 0
		self.numberOfTimesAsleepDuringMinute = {}

	def addSleepInterval(self, fromMinute, toMinute):
		self.minutesAsleep += toMinute - fromMinute
		for minute in range(fromMinute, toMinute):
			try:
				self.numberOfTimesAsleepDuringMinute[minute] += 1
			except KeyError:
				self.numberOfTimesAsleepDuringMinute[minute] = 1

	def getMinuteMostOftenAsleep(self):
		if self.minutesAsleep == 0:
			# Not sure what's best to return in this case
			return 0
		dictItems = self.numberOfTimesAsleepDuringMinute.items()
		minute = sorted(dictItems, key=lambda item: item[1], reverse=True)[0][0]
		return minute

class Event:
	def __init__(self, date, minute, text):
		self.date = date
		self.minute = int(minute)
		self.text = text

	@staticmethod
	def createFromString(s):
		date = s.split()[0][1:]
		minute = s.split()[1].split(":")[1].split("]")[0]
		text = s.split(None, 2)[2]
		return Event(date, minute, text)

#############
# Functions #
#############
# Reads a file and returns a list of Event (in chronological order).
def getEventsFromFile(fileName):
	with open("input04") as f:
		return [Event.createFromString(s) for s in sorted(f.readlines())]

# Processes the events in "events", and returns a dict containing data about guards
# (key: guard ID, value: Guard object)
def getGuardDataFromEvents(events):
	idToGuard = {}
	currentGuard = None
	asleepFrom = None
	for event in events:
		if re.match("^Guard #", event.text):
			guardID = event.text.split()[1][1:]
			try:
				currentGuard = idToGuard[guardID]
			except KeyError:
				currentGuard = Guard(guardID)
				idToGuard[guardID] = currentGuard
		elif re.match("^falls asleep", event.text):
			asleepFrom = event.minute
		elif re.match("^wakes up", event.text):
			asleepTo = event.minute
			currentGuard.addSleepInterval(asleepFrom, asleepTo)
	return idToGuard

def findMostSleepyGuard(guards):
	guard = sorted(guards, key=lambda x: x.minutesAsleep, reverse=True)[0]
	minuteMostOftenAsleep = guard.getMinuteMostOftenAsleep()
	print("Guard {id} slept the most in total. Most often asleep during minute {minute}.".format(
			id=guard.id, minute=minuteMostOftenAsleep))
	print("Answer to part 1: {}".format(guard.id * minuteMostOftenAsleep))

def findGuardThatSleptTheMostDuringASingleMinute(guards):
	guardTuples = []
	for guard in guards:
		minute = guard.getMinuteMostOftenAsleep()
		try:
			numberOfTimesAsleep = guard.numberOfTimesAsleepDuringMinute[minute]
		except KeyError:
			numberOfTimesAsleep = 0
		guardTuples.append((guard.id, minute, numberOfTimesAsleep))
	guardTuple = sorted(guardTuples, key=lambda tuple: tuple[2], reverse=True)[0]
	print("Guard {id} slept the most during a given minute (minute {minute})".format(
			id=guardTuple[0], minute=guardTuple[1]))
	print("Answer to part 2: {}".format(guardTuple[0] * guardTuple[1]))

########
# Main #
########
idToGuard = getGuardDataFromEvents(getEventsFromFile("input04"))

# Part 1
findMostSleepyGuard(idToGuard.values())

# Part 2
findGuardThatSleptTheMostDuringASingleMinute(idToGuard.values())
