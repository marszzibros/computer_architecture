import numpy as np



def fetch():
    pass
def decode():
    pass
def execute():
    pass

instruction_dict = {"NOOP"  : [0, 0, 0, 0],
                    "ADD"   : [0, 0, 0, 1],
                    "ADDI"  : [0, 0, 1, 0],
                    ""}

instruction = np.zeros(32, dtype=int)
mem = np.empty(1000)
