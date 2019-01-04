import sys

from dec16.cpu import CPU, InstructionExample
from dec16.parser import getInstructionsAndExamplesFromFile

if __name__ == "__main__":
	cpu = CPU()
	(instructions, instructionExamples) = getInstructionsAndExamplesFromFile("input16.txt")
	
	# Part 1
	part1Answer = len([x for x in instructionExamples if cpu.getNumberOfMatchingOperations(x) >= 3])
	print("Number of instructions that matches at least 3 operations: {}".format(part1Answer))
	
	# Part 2
	cpu.executeInstructions(instructions)
	print("After executing all instructions, register 0 contains {}".format(cpu.registers[0]))
