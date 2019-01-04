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

allOperations = [
	Operation(calcValueAddr), Operation(calcValueAddi),
	Operation(calcValueMulr), Operation(calcValueMuli),
	Operation(calcValueBanr), Operation(calcValueBani),
	Operation(calcValueBorr), Operation(calcValueBori),
	Operation(calcValueSetr), Operation(calcValueSeti),
	Operation(calcValueGtir), Operation(calcValueGtri), Operation(calcValueGtrr),
	Operation(calcValueEqir), Operation(calcValueEqri), Operation(calcValueEqrr)
]
