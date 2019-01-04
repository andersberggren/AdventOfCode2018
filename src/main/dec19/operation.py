class Operation:
	nameToOperation = {}
	
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

Operation.nameToOperation = {
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
