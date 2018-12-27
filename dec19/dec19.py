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

	def executeInstructionsUntilHaltPart1(self):
		i = 0
		while True:
			try:
				instruction = self.instructions[self.registers[self.ip]]
			except IndexError:
				break
			operation = self.nameToOperation[instruction[0]]
			operation.execInstruction(self.registers, instruction)
			self.registers[self.ip] += 1
			i += 1
		print("CPU halted after {i} cycles. Registers: {r}".format(i=i, r=self.registers))

	def executeInstructionsUntilHaltPart2(self):
		i = 0
		while True:
			# Shortcuts
			if self.registers[1] == 9 and self.registers[2] == 10551403:
				if self.registers[3] > 0 \
						and (self.registers[3] * self.registers[5] < self.registers[2]) \
						and (self.registers[2] % self.registers[3] == 0):
					# Path 1
					print("Shortcut 1")
					self.registers[5] = self.registers[2] // self.registers[3]
				elif self.registers[5] <= self.registers[2]:
					# Path 2, will loop as long as:
					#   (reg[3]+1) <= reg[2]
					#   (reg[3]+1) * reg[5] < reg[2]
					# Each loop will increase reg[3] by 1
					newReg3 = self.registers[3]
					while newReg3+1 <= self.registers[2] \
							and self.registers[2] % (newReg3+1) != 0:
						newReg3 += 1
					if newReg3 == self.registers[3]:
						# Path 2a
						print("Shortcut 2a")
						self.registers[5] = self.registers[2]+1
					else:
						# Path 2b
						print("Shortcut 2b")
						self.registers[3] = newReg3
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
(instructionPointer, instructions) = getInstructionPointerAndInstructionsFromFile("input19.txt")

# Part 1
cpu = CPU(instructionPointer, instructions)
cpu.executeInstructionsUntilHaltPart1()

# Part 2
cpu = CPU(instructionPointer, instructions)
cpu.registers[0] = 1
cpu.executeInstructionsUntilHaltPart2()
