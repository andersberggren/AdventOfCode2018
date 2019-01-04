import sys

from dec16.cpu import InstructionExample, allOperations
from dec16.parser import getInstructionsAndExamplesFromFile

#############
# Functions #
#############
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
if __name__ == "__main__":
	(instructions, instructionExamples) = getInstructionsAndExamplesFromFile("input16.txt")
	
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
