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
print(bin(5))
instr = build_instruction(5, 5, 5, 5, 5)
print(bin((instr >> 28) & 15))
opcode = (instr >> 28) & 15
Rd = (instr >> 24) & 15
Rs1 = (instr >> 20) & 15
Rs2 = (instr >> 16) & 15
immed = instr & 15

print(opcode)
print(Rd)
print(Rs1)
print(Rs2)
print(immed)