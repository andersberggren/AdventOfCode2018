import re
import sys

#########
# Class #
#########
class Operation:
	def __init__(self, calcValue):
		self.calcValue = calcValue

	def execInstruction(self, registers, instruction):
		registerA = registers[instruction[1]]
		registerB = registers[instruction[2]]
		valueA = instruction[1]
		valueB = instruction[2]
		registerC = self.calcValue(registerA, registerB, valueA, valueB)
		registers[instruction[3]] = registerC

class InstructionExample:
	def __init__(self, registersBefore, instruction, registersAfter):
		self.registersBefore = registersBefore
		self.instruction = instruction
		self.registersAfter = registersAfter

#############
# Functions #
#############
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

def calcValueAddr(registerA, registerB, valueA, valueB):
	return registerA + registerB

def calcValueAddi(registerA, registerB, valueA, valueB):
	return registerA + valueB

def calcValueMulr(registerA, registerB, valueA, valueB):
	return registerA * registerB

def calcValueMuli(registerA, registerB, valueA, valueB):
	return registerA * valueB

def calcValueBanr(registerA, registerB, valueA, valueB):
	return registerA & registerB

def calcValueBani(registerA, registerB, valueA, valueB):
	return registerA & valueB

def calcValueBorr(registerA, registerB, valueA, valueB):
	return registerA | registerB

def calcValueBori(registerA, registerB, valueA, valueB):
	return registerA | valueB

def calcValueSetr(registerA, registerB, valueA, valueB):
	return registerA

def calcValueSeti(registerA, registerB, valueA, valueB):
	return valueA

def calcValueGtir(registerA, registerB, valueA, valueB):
	if valueA > registerB:
		return 1
	else:
		return 0

def calcValueGtri(registerA, registerB, valueA, valueB):
	if registerA > valueB:
		return 1
	else:
		return 0

def calcValueGtrr(registerA, registerB, valueA, valueB):
	if registerA > registerB:
		return 1
	else:
		return 0

def calcValueEqir(registerA, registerB, valueA, valueB):
	if valueA == registerB:
		return 1
	else:
		return 0

def calcValueEqri(registerA, registerB, valueA, valueB):
	if registerA == valueB:
		return 1
	else:
		return 0

def calcValueEqrr(registerA, registerB, valueA, valueB):
	if registerA == registerB:
		return 1
	else:
		return 0

# Returns number of matching operations for instructionExample.
def getNumberOfMatchingOperations(instructionExample):
	nMatches = 0
	for operation in allOperations:
		registers = list(instructionExample.registersBefore)
		operation.execInstruction(registers, instructionExample.instruction)
		if registers == instructionExample.registersAfter:
			nMatches += 1
	return nMatches

# Returns dict, where key is opcode (integer), and value is a list of operations that match.
def getOpcodeToOperationList(instructionExamples):
	opcodeToOperationList = {}
	for ie in instructionExamples:
		opcode = ie.instruction[0]
		if opcode not in opcodeToOperationList:
			# First time encountering this opcode. Initially, all operations could match.
			opcodeToOperationList[opcode] = list(allOperations)
		for operation in allOperations:
			registers = list(ie.registersBefore)
			operation.execInstruction(registers, ie.instruction)
			if registers != ie.registersAfter:
				# This operation doesn't match this InstructionExample,
				# so this opcode can't be this operation.
				try:
					opcodeToOperationList[opcode].remove(operation)
				except ValueError:
					# Operation has already been removed from list
					pass
	return opcodeToOperationList

def solveOpcodes(opcodeToOperationList):
	# Dict. Key is opcode. Value is the only possible operation.
	opcodeToOperation = {opcode: opList[0] for (opcode, opList) in opcodeToOperationList.items() if len(opList) == 1}
	solvedOpcodes = set(opcodeToOperation.keys())
	solvedOperations = set(opcodeToOperation.values())
	progress = False
	for opcode in [x for x in opcodeToOperationList if x not in solvedOpcodes]:
		for operation in solvedOperations:
			try:
				opcodeToOperationList[opcode].remove(operation)
				progress = True
			except ValueError:
				# Operation has already been removed from list
				pass
	if not progress:
		print("Couldn't solve opcodes")
		sys.exit(1)
	solved = all([len(opList) == 1 for opList in opcodeToOperationList.values()])
	if not solved:
		solveOpcodes(opcodeToOperationList)

# Executes the instructions in "instructions".
# Returns the registers.
def executeInstructions(instructions, opcodeToOperation):
	registers = [0, 0, 0, 0]
	for instruction in instructions:
		operation = opcodeToOperation[instruction[0]]
		operation.execInstruction(registers, instruction)
	return registers

def printOpcodeToOperationList(opcodeToOperationList):
	for opcode in sorted(opcodeToOperationList):
		operationNames = ", ".join([x.name for x in opcodeToOperationList[opcode]])
		print("opcode {oc} matches: {ol}".format(oc=opcode, ol=operationNames))

########
# Main #
########
allOperations = [
	Operation(calcValueAddr), Operation(calcValueAddi),
	Operation(calcValueMulr), Operation(calcValueMuli),
	Operation(calcValueBanr), Operation(calcValueBani),
	Operation(calcValueBorr), Operation(calcValueBori),
	Operation(calcValueSetr), Operation(calcValueSeti),
	Operation(calcValueGtir), Operation(calcValueGtri), Operation(calcValueGtrr),
	Operation(calcValueEqir), Operation(calcValueEqri), Operation(calcValueEqrr)
]
(instructions, instructionExamples) = getInstructionsAndExamplesFromFile("input16")

# Part 1
ieToNumberOfMatchingOperations = {ie: getNumberOfMatchingOperations(ie) for ie in instructionExamples}
part1Answer = len([x for x in ieToNumberOfMatchingOperations.values() if x >= 3])
print("Part 1. Number of instructions that matches at least 3 operations: {}".format(part1Answer))

# Part 2
opcodeToOperationList = getOpcodeToOperationList(instructionExamples)
solveOpcodes(opcodeToOperationList)
opcodeToOperation = {opcode: opList[0] for (opcode, opList) in opcodeToOperationList.items()}
registers = executeInstructions(instructions, opcodeToOperation)
print("Part 2. Register 0 contains: {}".format(registers[0]))
