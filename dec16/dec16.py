import re
import sys

#########
# Class #
#########
class Operation:
	def __init__(self, registers, instruction):
		self.registers = registers
		self.instruction = instruction

	def getRegA(self):
		return self.registers[self.instruction[1]]

	def getRegB(self):
		return self.registers[self.instruction[2]]

	def getValueA(self):
		return self.instruction[1]

	def getValueB(self):
		return self.instruction[2]

	def setRegC(self, value):
		self.registers[self.instruction[3]] = value

class InstructionExample:
	def __init__(self, registersBefore, instruction, registersAfter):
		self.registersBefore = registersBefore
		self.instruction = instruction
		self.registersAfter = registersAfter

#############
# Functions #
#############
# Returns (instructions, examples), where:
# - instructions is a list. Each element in the list (an instruction) is a list of integers.
# - examples is a list of InstructionExample.
def getInstructionsAndExamplesFromFile(fileName):
	instructions = []
	examples = []
	with open(fileName) as f:
		line = None
		while line != "":
			line = f.readline()
			matchBefore = re.match("^Before: *(\[.*\])", line)
			if matchBefore:
				registersBefore = stringToIntegerList(matchBefore.group(1))
				line = f.readline()
				instruction = stringToIntegerList(line)
				line = f.readline()
				matchAfter = re.match("^After: *(\[.*\])", line)
				registersAfter = stringToIntegerList(matchAfter.group(1))
				examples.append(InstructionExample(registersBefore, instruction, registersAfter))
			elif len(line.strip()) > 0:
				instructions.append(stringToIntegerList(line))
	return (instructions, examples)

# Supported string formats:
# 1:  [1, 2, 3, 4] (Comma-separated with square brackets)
# 2:  1 2 3 4      (Whitespace-separated without square brackets)
# Returns a list of integers.
def stringToIntegerList(s):
	if "[" in s:
		return [int(x.strip()) for x in s.strip("\[\]").split(",")]
	else:
		return [int(x.strip()) for x in s.split()]

def opAddr(registers, instruction):
	opAddr.name = "addr"
	op = Operation(registers, instruction)
	op.setRegC(op.getRegA() + op.getRegB())

def opAddi(registers, instruction):
	opAddi.name = "addi"
	op = Operation(registers, instruction)
	op.setRegC(op.getRegA() + op.getValueB())

def opMulr(registers, instruction):
	opMulr.name = "mulr"
	op = Operation(registers, instruction)
	op.setRegC(op.getRegA() * op.getRegB())

def opMuli(registers, instruction):
	opMuli.name = "muli"
	op = Operation(registers, instruction)
	op.setRegC(op.getRegA() * op.getValueB())

def opBanr(registers, instruction):
	opBanr.name = "banr"
	op = Operation(registers, instruction)
	op.setRegC(op.getRegA() & op.getRegB())

def opBani(registers, instruction):
	opBani.name = "bani"
	op = Operation(registers, instruction)
	op.setRegC(op.getRegA() & op.getValueB())

def opBorr(registers, instruction):
	opBorr.name = "borr"
	op = Operation(registers, instruction)
	op.setRegC(op.getRegA() | op.getRegB())

def opBori(registers, instruction):
	opBori.name = "bori"
	op = Operation(registers, instruction)
	op.setRegC(op.getRegA() | op.getValueB())

def opSetr(registers, instruction):
	opSetr.name = "setr"
	op = Operation(registers, instruction)
	op.setRegC(op.getRegA())

def opSeti(registers, instruction):
	opSeti.name = "seti"
	op = Operation(registers, instruction)
	op.setRegC(op.getValueA())

def opGtir(registers, instruction):
	opGtir.name = "gtir"
	op = Operation(registers, instruction)
	if op.getValueA() > op.getRegB():
		op.setRegC(1)
	else:
		op.setRegC(0)

def opGtri(registers, instruction):
	opGtri.name = "gtri"
	op = Operation(registers, instruction)
	if op.getRegA() > op.getValueB():
		op.setRegC(1)
	else:
		op.setRegC(0)

def opGtrr(registers, instruction):
	opGtrr.name = "gtrr"
	op = Operation(registers, instruction)
	if op.getRegA() > op.getRegB():
		op.setRegC(1)
	else:
		op.setRegC(0)

def opEqir(registers, instruction):
	opEqir.name = "eqir"
	op = Operation(registers, instruction)
	if op.getValueA() == op.getRegB():
		op.setRegC(1)
	else:
		op.setRegC(0)

def opEqri(registers, instruction):
	opEqri.name = "eqri"
	op = Operation(registers, instruction)
	if op.getRegA() == op.getValueB():
		op.setRegC(1)
	else:
		op.setRegC(0)

def opEqrr(registers, instruction):
	opEqrr.name = "eqrr"
	op = Operation(registers, instruction)
	if op.getRegA() == op.getRegB():
		op.setRegC(1)
	else:
		op.setRegC(0)

# Returns number of matching operations for instructionExample.
def getNumberOfMatchingOperations(instructionExample):
	nMatches = 0
	for operation in allOperations:
		registers = list(instructionExample.registersBefore)
		operation(registers, instructionExample.instruction)
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
			operation(registers, ie.instruction)
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
		operation(registers, instruction)
	return registers

def printOpcodeToOperationList(opcodeToOperationList):
	for opcode in sorted(opcodeToOperationList):
		operationNames = ", ".join([x.name for x in opcodeToOperationList[opcode]])
		print("opcode {oc} matches: {ol}".format(oc=opcode, ol=operationNames))

########
# Main #
########
allOperations = [
	opAddr, opAddi, opMulr, opMuli, opBanr, opBani, opBorr, opBori,
	opSetr, opSeti, opGtir, opGtri, opGtrr, opEqir, opEqri, opEqrr
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
