import re

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
def getInstructionExamplesFromFile(fileName):
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
	return examples

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

########
# Main #
########
allOperations = [opAddr, opAddi, opMulr, opMuli, opBanr, opBani, opBorr, opBori,
	opSetr, opSeti, opGtir, opGtri, opGtrr, opEqir, opEqri, opEqrr]

instructionExamples = getInstructionExamplesFromFile("input16")
#print("Number of instruction examples: {}".format(len(instructionExamples)))

# Dict. Key is InstructionExample. Value is number of operations that match.
ieToCount = {}

for ie in instructionExamples:
	ieToCount[ie] = 0
	for operation in allOperations:
		registers = list(ie.registersBefore)
		operation(registers, ie.instruction)
		if registers == ie.registersAfter:
			ieToCount[ie] += 1

part1Answer = len([x for x in ieToCount.values() if x >= 3])
print("Part 1. Number of instructions that matches at least 3 operations: {}".format(part1Answer))
