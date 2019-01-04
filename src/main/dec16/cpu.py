class CPU:
	allOperations = set()
	
	def __init__(self):
		self.registers = [0, 0, 0, 0]
		# Dict. Key is opcode (int). Value is a set of Operation that the opcode could represent.
		self.opcodeToMatchingOperations = {}
		# Dict. Key is opcode (int). Value is corresponding Operation.
		self.opcodeToOperation = {}
	
	def executeInstructions(self, instructions):
		if not self.areAllOpcodesSolved():
			raise RuntimeError("All opcodes aren't solved")
		for instruction in instructions:
			opcode = instruction[0]
			operation = self.opcodeToOperation[opcode]
			operation.execInstruction(self.registers, instruction)
	
	def getNumberOfMatchingOperations(self, instructionExample):
		opcode = instructionExample.instruction[0]
		if opcode not in self.opcodeToMatchingOperations:
			# First time encountering this opcode. Initially, all operations could match.
			self.opcodeToMatchingOperations[opcode] = set(CPU.allOperations)
		nMatches = 0
		for operation in CPU.allOperations:
			tempRegisters = list(instructionExample.registersBefore)
			operation.execInstruction(tempRegisters, instructionExample.instruction)
			if tempRegisters == instructionExample.registersAfter:
				nMatches += 1
			else:
				try:
					self.opcodeToMatchingOperations[opcode].remove(operation)
				except KeyError:
					pass
		self.trySolveOpcodes()
		return nMatches
	
	def trySolveOpcodes(self):
		self.updateSolvedOpcodes()
		solvedOpcodes = set(self.opcodeToOperation.keys())
		solvedOperations = set(self.opcodeToOperation.values())
		progress = False
		for opcode in [x for x in self.opcodeToMatchingOperations if x not in solvedOpcodes]:
			if len(self.opcodeToMatchingOperations[opcode] & solvedOperations) > 0:
				self.opcodeToMatchingOperations[opcode] -= solvedOperations
				progress = True
		self.updateSolvedOpcodes()
		if progress and not self.areAllOpcodesSolved():
			self.trySolveOpcodes()
	
	def updateSolvedOpcodes(self):
		self.opcodeToOperation = {
			opcode: next(iter(operations))
			for (opcode, operations) in self.opcodeToMatchingOperations.items()
			if len(operations) == 1
		}
	
	def areAllOpcodesSolved(self):
		return len(self.opcodeToOperation) == len(self.opcodeToMatchingOperations)

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

CPU.allOperations = {
	Operation(calcValueAddr), Operation(calcValueAddi),
	Operation(calcValueMulr), Operation(calcValueMuli),
	Operation(calcValueBanr), Operation(calcValueBani),
	Operation(calcValueBorr), Operation(calcValueBori),
	Operation(calcValueSetr), Operation(calcValueSeti),
	Operation(calcValueGtir), Operation(calcValueGtri), Operation(calcValueGtrr),
	Operation(calcValueEqir), Operation(calcValueEqri), Operation(calcValueEqrr)
}
