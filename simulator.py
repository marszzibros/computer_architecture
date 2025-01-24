import numpy as np
from microprocessor import CPU, Instruction
from data_utils import read_instruction, parse_instruction

MEM_SIZE = 65536
NUM_REGISTERS = 16

instruction_path = "instruction.txt"

instructions = []
pc = 100
cpu = CPU(pc, MEM_SIZE, NUM_REGISTERS)

for index, line in enumerate(read_instruction(instruction_path)):
    instruction = parse_instruction(line)

    cpu.memory[pc + index] = instruction

while True:
    instruction = cpu.fetch()
    instruction = cpu.decode(instruction)

    status = cpu.execute(instruction)
    if status == 1:
        break
    cpu.pc = cpu.next_pc

print(cpu.registers)
print(cpu.memory[26])
