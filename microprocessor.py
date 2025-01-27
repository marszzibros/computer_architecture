# Jay Hwasung Jung (jjung2)
# Computer Architecture

# microprocessor.py
# Instruction and CPU classes

import numpy as np

class Instruction:
    def __init__(self, opcode, Rd, Rs1, Rs2, immed):
        self.opcode = opcode
        self.Rd = Rd
        self.Rs1 = Rs1
        self.Rs2 = Rs2
        self.immed = immed


class CPU:
    def __init__(self, pc, memory_size, num_registers):
        self.pc = pc
        self.next_pc = None
        self.memory = np.zeros(memory_size, dtype=int)
        self.registers = np.zeros(num_registers, dtype=int)

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
        immed = instruction & 31
        
        # AND operator with 16 (10000) to check if the number is negative
        if immed & 16:
            # signed integer
            immed = - (2**5 - immed)

        # create an instance of Instruction
        return Instruction(opcode, Rd, Rs1, Rs2, immed)
    
    def execute(self, instruction):
        # NOOP
        if instruction.opcode == 0:
            pass

        # ADD and ADDI 
        elif instruction.opcode == 1 or instruction.opcode == 2:
            if instruction.opcode == 1:
                
                alu_result = self.registers[instruction.Rs1] + self.registers[instruction.Rs2]
            elif instruction.opcode == 2:
                alu_result = self.registers[instruction.Rs1] + instruction.immed

            if instruction.Rd != 0:
                self.registers[instruction.Rd] = alu_result
            
        # BEQ
        elif instruction.opcode == 3:
            if self.registers[instruction.Rs1] == self.registers[instruction.Rs2]:
                self.next_pc = self.pc + instruction.immed
            else:
                pass
        
        # JAL
        elif instruction.opcode == 4:
            alu_result = self.pc + 1
            if instruction.Rd != 0:
                self.registers[instruction.Rd] = alu_result
            self.next_pc = self.pc + instruction.immed

        # LW
        elif instruction.opcode == 5:
            eff_address = self.registers[instruction.Rs1] + instruction.immed
            if instruction.Rd != 0:
                self.registers[instruction.Rd] = self.memory[eff_address]
    
        # SW
        elif instruction.opcode == 6:
            eff_address = self.registers[instruction.Rs2] + instruction.immed
            self.memory[eff_address] = self.registers[instruction.Rs1]
            pass
        
        # RETURN
        elif instruction.opcode == 7:
            return 1
        
        else:
            raise("Invalid opcode")
        
        return 0

    
