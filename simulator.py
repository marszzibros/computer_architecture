# Jay Hwasung Jung (jjung2)
# Computer Architecture

# simulator.py
# tester for assignment1

import numpy as np
from microprocessor import CPU
from data_utils import read_instruction, parse_instruction

MEM_SIZE = 65536
NUM_REGISTERS = 16

instruction_path = "instruction.txt"

instructions = []
pc = 100

# create CPU instance
cpu = CPU(pc, MEM_SIZE, NUM_REGISTERS)

# read instructions line by line and store them in memory in CPU instance
for index, line in enumerate(read_instruction(instruction_path)):
    instruction = parse_instruction(line)
    cpu.memory[pc + index] = instruction

# run instructions
while True:

    # fetch 
    instruction = cpu.fetch()
    
    # decode
    instruction = cpu.decode(instruction)
    
    # execute
    status = cpu.execute(instruction)

    if status == 1:
        break

    cpu.pc = cpu.next_pc

# print registers; The answer for the graduate loop challenge 
# should be in the R1 which is cpu.registers[1]
print(cpu.registers)

