import numpy as np
from microprocessor import CPU, Instruction

MEM_SIZE = 65536
NUM_REGISTERS = 16

# A function that builds insturction
def build_instruction(opcode, Rd, Rs1, Rs2, immed):
    instr = opcode << 28
    if Rd is not None:
        instr = instr + (Rd << 24)
    if Rs1 is not None:
        instr = instr + (Rs1 << 20)
    if Rs2 is not None:
        instr = instr + (Rs2 << 16)
    if immed is not None:
        instr = instr + immed
    return instr

# Assign constant values to represent opcodes
opcode_dict = { "NOOP"  : 0,    
                "ADD"   : 1,   
                "ADDI"  : 2,    
                "BEQ"   : 3,
                "JAL"   : 4,
                "LW"    : 5,
                "SW"    : 6,
                "RETURN": 7}
