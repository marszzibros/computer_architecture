import numpy as np

class Instruction:
    def __init__(self, opcode, Rd, Rs1, Rs2, immed):
        self.opcode = opcode
        self.Rd = Rd
        self.Rs1 = Rs1
        self.Rs2 = Rs2
        self.immed = immed

        # Assign constant values to represent opcodes
        self.opcode_dict = {"NOOP"  : 0,    
                            "ADD"   : 1,   
                            "ADDI"  : 2,    
                            "BEQ"   : 3,
                            "JAL"   : 4,
                            "LW"    : 5,
                            "SW"    : 6,
                            "RETURN": 7}


    def instruction(self):
        pass

class CPU:
    def __init__(self, pc, next_pc, memory, registers):
        self.pc = pc
        self.next_pc = next_pc
        self.memory = np.zeros(memory, dtype=int)
        self.registers = np.zeros(registers, dtype=int)

    def fetch(self):
        # Read the instruction at location mem[pc]
        instruction = self.memory[self.pc]

        # Set next_pc to pc + 1
        self.next_pc = self.pc + 1

        return instruction
    
    def decode(self,):
        pass
    def execute(self,):
        pass

    
