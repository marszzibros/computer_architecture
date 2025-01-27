# Jay Hwasung Jung (jjung2)
# Computer Architecture

# data_utils.py
# build_instruction, parse_instruction, read_instruction functions


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
        if immed < 0:
            # From -(2^N - b) = (signed int)
            immed = 2**5 - abs(immed)
        instr = instr + immed
    return instr

def parse_instruction(line):
    # initialize variables
    opcode_dict = { "NOOP"  : 0,    
                "ADD"   : 1,   
                "ADDI"  : 2,    
                "BEQ"   : 3,
                "JAL"   : 4,
                "LW"    : 5,
                "SW"    : 6,
                "RETURN": 7}
    
    opcode = 0
    Rd = 0
    Rs1 = 0   
    Rs2 = 0
    immed = 0 
    
    # split by space after removing comments
    line = line.rstrip('\n').split('#')[0].strip(' ').split(' ')
    
    # OPCODE to upper letter case
    line[0] = line[0].upper()
    opcode = opcode_dict[line[0]]

    # parse NOOP and RETURN
    if opcode == 0 or opcode == 7:

        # only opcode
        if len(line) != 1:
            raise ValueError(f"{line[0]} should not have any arguments")
    
    # parse ADD
    elif opcode == 1:

        # opcode rd rs1 rs2
        if len(line) != 4:
            raise ValueError("ADD should have Rd, Rs1, Rs2")
        else:
            if 'R' not in line[1].upper() or 'R' not in line[2].upper() or 'R' not in line[3].upper():
                raise ValueError("ADD should have Rd, Rs1, Rs2")
            else:
                Rd = int(line[1][1:-1])
                Rs1 = int(line[2][1:-1])
                Rs2 = int(line[3][1:])

                # check if it is valid register number
                if Rd >= NUM_REGISTERS or Rs1 >= NUM_REGISTERS or Rs2 >= NUM_REGISTERS:
                    raise ValueError(f"Register number should be less than {NUM_REGISTERS}")
    
    # parse ADDI
    elif opcode == 2:
        if len(line) != 4:
            raise ValueError("ADDI should have Rd, Rs1, immed")
        else:
            if 'R' not in line[1].upper() or 'R' not in line[2].upper():
                raise ValueError("ADDI should have Rd, Rs1, immed")
            else:
                Rd = int(line[1][1:-1])
                Rs1 = int(line[2][1:-1])
                immed = int(line[3])

                # check if it is valid register number
                if Rd >= NUM_REGISTERS or Rs1 >= NUM_REGISTERS:
                    raise ValueError(f"Register number should be less than {NUM_REGISTERS}")

    # parse BEQ
    elif opcode == 3:
        if len(line) != 4:
            raise ValueError("BEQ should have Rs1, Rs2, immed")
        else:
            if 'R' not in line[1].upper() or 'R' not in line[2].upper():
                raise ValueError("ADDI should have Rd, Rs1, immed")
            else:
                Rs1 = int(line[1][1:-1])
                Rs2 = int(line[2][1:-1])
                immed = int(line[3])
                
                # check if it is valid register number
                if Rs1 >= NUM_REGISTERS or Rs1 >= NUM_REGISTERS:
                    raise ValueError(f"Register number should be less than {NUM_REGISTERS}")

    # parse JAL
    elif opcode == 4:
        if len(line) != 3:
            raise ValueError("JAL should have Rd, immed")
        else:
            if 'R' not in line[1].upper():
                raise ValueError("JAL should have Rd, immed")
            else:
                Rd = int(line[1][1:-1])
                immed = int(line[2])
                if Rd >= NUM_REGISTERS:
                    raise ValueError(f"Register number should be less than {NUM_REGISTERS}")
    
    # parse LW
    elif opcode == 5:
        if len(line) != 3:
            raise ValueError(f"{line[0]} should have three parameters")
        
        if 'R' not in line[1].upper() or 'R' not in line[2].upper():
            raise ValueError(f"Invalid parameters for {line[0]}")
        
        # Remove ( and ) from the string
        immed_r = line[2].split('(')
        immed_r[1] = immed_r[1][:-1]
        immed = int(immed_r[0])

        Rd = int(line[1][1:-1])
        Rs1 = int(immed_r[1][1:])
        if Rd >= NUM_REGISTERS or Rs1 >= NUM_REGISTERS:
            raise ValueError(f"Register number should be less than {NUM_REGISTERS}")
    
    # parse SW
    elif opcode == 6:
        if len(line) != 3:
            raise ValueError(f"{line[0]} should have three parameters")
        
        if 'R' not in line[1].upper() or 'R' not in line[2].upper():
            raise ValueError(f"Invalid parameters for {line[0]}")
        
        # Remove ( and ) from the string
        immed_r = line[2].split('(')
        immed_r[1] = immed_r[1][:-1]
        immed = int(immed_r[0])

        Rs1 = int(line[1][1:-1])
        Rs2 = int(immed_r[1][1:])
        if Rs1 >= NUM_REGISTERS or Rs2 >= NUM_REGISTERS:
            raise ValueError(f"Register number should be less than {NUM_REGISTERS}")
    
    return build_instruction(opcode, Rd, Rs1, Rs2, immed)               

# read instructions from a file
def read_instruction(file_path = "instruction.txt"):
    with open(file_path, 'r') as file:
        instructions = file.readlines()
    return instructions
