import re

from dec16.cpu import InstructionExample

# Returns (instructions, instructionExamples), where:
# - instructions is a list. Each element in the list (an instruction) is a list of integers.
# - instructionExamples is a list of InstructionExample.
def getInstructionsAndExamplesFromFile(fileName):
	instructions = []
	instructionExamples = []
	with open(fileName) as f:
		lines = f.readlines()
		while len(lines) > 0:
			line = lines.pop(0)
			matchBefore = re.match("^Before: *(\[.*\])", line)
			if matchBefore:
				registersBefore = stringToIntegerList(matchBefore.group(1))
				instruction = stringToIntegerList(lines.pop(0))
				matchAfter = re.match("^After: *(\[.*\])", lines.pop(0))
				registersAfter = stringToIntegerList(matchAfter.group(1))
				instructionExample = InstructionExample(registersBefore, instruction, registersAfter)
				instructionExamples.append(instructionExample)
			elif len(line.strip()) > 0:
				instructions.append(stringToIntegerList(line))
	return (instructions, instructionExamples)

# Supported string formats:
# 1:  [1, 2, 3, 4] (Comma-separated with square brackets)
# 2:  1 2 3 4      (Whitespace-separated without square brackets)
# Returns a list of integers.
def stringToIntegerList(s):
	if "[" in s:
		return [int(x.strip()) for x in s.strip("\[\]").split(",")]
	else:
		return [int(x.strip()) for x in s.split()]
