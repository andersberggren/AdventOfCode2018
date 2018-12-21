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
				instruction = [int(x) for x in line.strip().split()]
				line = f.readline()
				matchAfter = re.match("^After: *(\[.*\])", line)
				registersAfter = stringToIntegerList(matchAfter.group(1))
				examples.append(InstructionExample(registersBefore, instruction, registersAfter))
			elif len(line.strip()) > 0:
				instructions.append([int(x) for x in line.strip().split()])
	return (instructions, examples)

def stringToIntegerList(s):
	return [int(x.strip()) for x in s.strip("\[\]").split(",")]

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

# Returns dict, where key i InstructionExample, and value is number of operations that match.
def getNumberOfMatchingOperations(instructionExamples):
	ieToCount = {}
	for ie in instructionExamples:
		ieToCount[ie] = 0
		for operation in allOperations:
			registers = list(ie.registersBefore)
			operation(registers, ie.instruction)
			if registers == ie.registersAfter:
				ieToCount[ie] += 1
	return ieToCount

# Returns dict, where key is opcode (integer), and value is a list of operations that match.
def getPossibleOperationsForEachOpcode(instructionExamples):
	opcodeToOperationList = {}
	for ie in instructionExamples:
		opcode = ie.instruction[0]
		if opcode not in opcodeToOperationList:
			# First time encountering this opcode. All operations could potentially match.
			opcodeToOperationList[opcode] = list(allOperations)
		for operation in allOperations:
			registers = list(ie.registersBefore)
			operation(registers, ie.instruction)
			if registers != ie.registersAfter:
				# Operations doesn't match this InstructionExample, and can't be this opcode.
				try:
					opcodeToOperationList[opcode].remove(operation)
				except ValueError:
					# Operation has already been removed from list
					pass
	return opcodeToOperationList

def tryToSolve(opcodeToOperationList):
	# List of tuples: (opcode, operation)
	toRemove = []
	progress = False
	for (opcode, operationList) in opcodeToOperationList.items():
		if len(operationList) == 1:
			toRemove.append((opcode, operationList[0]))
	if len(toRemove) == 0:
		return False
	for (opcodeWithOnlyOneOperation, onlyOperation) in toRemove:
		for (opcode, operationList) in opcodeToOperationList.items():
			if opcode != opcodeWithOnlyOneOperation:
				try:
					operationList.remove(onlyOperation)
					progress = True
				except ValueError:
					# Operation has already been removed from list
					pass
	return progress

def printOpcodeToOperationList(opcodeToOperationList):
	for (opcode, operationList) in opcodeToOperationList.items():
		operationNames = ", ".join([x.name for x in operationList])
		print("opcode {oc} matches: {ol}".format(oc=opcode, ol=operationNames))

########
# Main #
########
allOperations = [
	opAddr, opAddi, opMulr, opMuli, opBanr, opBani, opBorr, opBori,
	opSetr, opSeti, opGtir, opGtri, opGtrr, opEqir, opEqri, opEqrr
]
(instructions, instructionExamples) = getInstructionsAndExamplesFromFile("input16")

part1Answer = len([x for x in getNumberOfMatchingOperations(instructionExamples).values() if x >= 3])
print("Part 1. Number of instructions that matches at least 3 operations: {}".format(part1Answer))

opcodeToOperationList = getPossibleOperationsForEachOpcode(instructionExamples)
printOpcodeToOperationList(opcodeToOperationList)
while tryToSolve(opcodeToOperationList):
	print("Tried to solve")
	printOpcodeToOperationList(opcodeToOperationList)

if not all([len(x) == 1 for x in opcodeToOperationList.values()]):
	print("Couldn't find solution")
	sys.exit(1)
opcodeToOperation = {opcode: opList[0] for (opcode, opList) in opcodeToOperationList.items()}

registers = [0, 0, 0, 0]
for instruction in instructions:
	operation = opcodeToOperation[instruction[0]]
	operation(registers, instruction)
print("Part 2. Register 0 contains: {}".format(registers[0]))
