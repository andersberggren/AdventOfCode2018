import re

#########
# Class #
#########
class Operation:
	def __init__(self, calcValue):
		self.calcValue = calcValue

	def execInstruction(self, registers, instruction):
		try:
			registerA = registers[instruction[1]]
		except IndexError:
			registerA = None
		try:
			registerB = registers[instruction[2]]
		except IndexError:
			registerB = None
		valueA = instruction[1]
		valueB = instruction[2]
		registerC = self.calcValue(registerA, registerB, valueA, valueB)
		registers[instruction[3]] = registerC

class CPU:
	def __init__(self, instructionPointer, instructions):
		self.registers = [0, 0, 0, 0, 0, 0]
		self.ip = instructionPointer
		self.instructions = instructions
		self.nameToOperation = {
			"addr": Operation(calcValueAddr),
			"addi": Operation(calcValueAddi),
			"mulr": Operation(calcValueMulr),
			"muli": Operation(calcValueMuli),
			"banr": Operation(calcValueBanr),
			"bani": Operation(calcValueBani),
			"borr": Operation(calcValueBorr),
			"bori": Operation(calcValueBori),
			"setr": Operation(calcValueSetr),
			"seti": Operation(calcValueSeti),
			"gtir": Operation(calcValueGtir),
			"gtri": Operation(calcValueGtri),
			"gtrr": Operation(calcValueGtrr),
			"eqir": Operation(calcValueEqir),
			"eqri": Operation(calcValueEqri),
			"eqrr": Operation(calcValueEqrr)
		}

	def executeInstructionsUntilHalt(self):
		i = 0
		while True:
			instructionIndex = self.registers[self.ip]
			if instructionIndex == 28:
				print("Currently at instruction 28. If register 0 had value {} the program would terminate now".format(self.registers[5]))
			try:
				instruction = self.instructions[self.registers[self.ip]]
			except IndexError:
				break
			operation = self.nameToOperation[instruction[0]]
			operation.execInstruction(self.registers, instruction)
			self.registers[self.ip] += 1
			i += 1
		print("CPU halted after {i} cycles. Registers: {r}".format(i=i, r=self.registers))

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

########
# Main #
########
(instructionPointer, instructions) = getInstructionPointerAndInstructionsFromFile("input21.txt")

cpu = CPU(instructionPointer, instructions)
cpu.registers[0] = 0
cpu.executeInstructionsUntilHalt()
