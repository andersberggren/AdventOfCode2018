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

	def executeInstructionsUntilHalt(self):
		i = 0
		registerStates = set()
		uniqueHaltValues = []
		while True:
			instructionIndex = self.registers[self.ip]
			if instructionIndex == 28:
				haltValue = self.registers[5]
				print("Cycle {i}. Value {h: >9} in register 0 would halt the program now. {r}".format(
						i=i, h=haltValue, r=self.registers))
				registerState = tuple(self.registers)
				if registerState in registerStates:
					print("Repeated register state. Loop found.")
					return
				else:
					registerStates.add(registerState)
				if haltValue in uniqueHaltValues:
					print("Repeated halt value. Latest unique halt value: {}".format(uniqueHaltValues[-1]))
				else:
					uniqueHaltValues.append(haltValue)
					print("Latest unique halt value: {}".format(uniqueHaltValues[-1]))
				print("{r} register states. {h} unique halt values.".format(
						r=len(registerStates), h=len(uniqueHaltValues)), flush=True)
			try:
				instruction = self.instructions[self.registers[self.ip]]
			except IndexError:
				break
			operation = instruction[0]
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
				instruction = [nameToOperation[matchInstruction.group(1)]]
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
nameToOperation = {
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
(instructionPointer, instructions) = getInstructionPointerAndInstructionsFromFile("input21.txt")

cpu = CPU(instructionPointer, instructions)
cpu.executeInstructionsUntilHalt()
