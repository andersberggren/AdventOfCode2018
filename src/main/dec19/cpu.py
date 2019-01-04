from dec19.operation import Operation

class CPU:
	def __init__(self, instructionPointer, instructions):
		self.registers = [0, 0, 0, 0, 0, 0]
		self.ip = instructionPointer
		self.instructions = instructions

	def executeInstructionsUntilHaltPart1(self):
		i = 0
		while True:
			try:
				instruction = self.instructions[self.registers[self.ip]]
			except IndexError:
				break
			operation = Operation.nameToOperation[instruction[0]]
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
			operation = Operation.nameToOperation[instruction[0]]
			operation.execInstruction(self.registers, instruction)
			self.registers[self.ip] += 1
			i += 1
		print("CPU halted after {i} cycles. Registers: {r}".format(i=i, r=self.registers))
