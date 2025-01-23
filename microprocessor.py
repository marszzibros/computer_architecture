import numpy as np

class Instruction:
    def __init__(self, opcode, Rd, Rs1, Rs2, immed):
        self.opcode = opcode
        self.Rd = Rd
        self.Rs1 = Rs1
        self.Rs2 = Rs2
        self.immed = immed


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
    
    def decode(self, instruction):

        # Decode values from an instruction
        opcode = (instruction >> 28) & 15
        Rd = (instruction >> 24) & 15
        Rs1 = (instruction >> 20) & 15
        Rs2 = (instruction >> 16) & 15
        immed = instruction & 15
        
        # create an instance of Instruction
        return Instruction(opcode, Rd, Rs1, Rs2, immed)
    
    def execute(self, instruction):
        if instruction.opcode == 0:
            pass 
        elif instruction.opcode == 1:
            self.registers[instruction.Rd] = self.registers[instruction.Rs1] + self.registers[instruction.Rs2]
        elif instruction.opcode == 2:
            self.registers[instruction.Rd] = self.registers[instruction.Rs1]
        elif instruction.opcode == 3:
            if self.registers[instruction.Rs1] == self.registers[instruction.Rs2]:
                self.next_pc = self.pc + instruction.immed
            else:
                pass
        elif instruction.opcode == 4:
            pass
        elif instruction.opcode == 5:
            pass
        elif instruction.opcode == 6:
            pass
        elif instruction.opcode == 7:
            pass
        else:
            print("Invalid opcode")

    
