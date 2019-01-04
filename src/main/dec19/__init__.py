import re

from dec19.cpu import CPU

#############
# Functions #
#############
# Returns (instructionPointer, instructions)
def getInstructionPointerAndInstructionsFromFile(fileName):
	instructionPointer = None
	instructions = []
	with open(fileName) as f:
		for line in f.readlines():
			matchIP = re.match("^#ip (\d+)", line)
			matchInstruction = re.match("^(\w+) (.*)", line)
			if matchIP:
				instructionPointer = int(matchIP.group(1))
			else:
				instruction = [matchInstruction.group(1)]
				instruction.extend([int(x) for x in matchInstruction.group(2).strip().split()])
				instructions.append(instruction)
	return (instructionPointer, instructions)

########
# Main #
########
if __name__ == "__main__":
	(instructionPointer, instructions) = getInstructionPointerAndInstructionsFromFile("input19.txt")
	
	# Part 1
	cpu = CPU(instructionPointer, instructions)
	cpu.executeInstructionsUntilHaltPart1()
	
	# Part 2
	cpu = CPU(instructionPointer, instructions)
	cpu.registers[0] = 1
	cpu.executeInstructionsUntilHaltPart2()
