import numpy as np
import math
from collections import deque


BITS_PER_BYTE = 8
WORD_BYTES = 4
MEM_SIZE = 64000
CACHE_BLOCKS = 2 ** 10
CACHE_PER_BLOCK = 2 ** 6
NUM_BLOCKS = CACHE_BLOCKS // CACHE_PER_BLOCK

# Since it is direct-mapped cache 
NUM_WAYS = 1
NUM_SETS  = NUM_BLOCKS // NUM_WAYS

class CacheBlock:
    def __init__(self, size):
        # integer tag
        self.tag = -1

        # data block bytearray
        self.block = bytearray(size)

class DMCache:
    def __init__(self, mem_size = 64000, word_bytes = 4, k = 1, cache_size = 2 ** 10, block_size = 2 ** 6, address_size = 16, file_name = "part-one-test.out"):
        self.file_name = file_name
        self.memory = np.zeros(mem_size, dtype=np.uint8)
        self.address_size = address_size
        self.word_bytes = word_bytes
        self.alignment = 256

        # define m
        m = mem_size / 4 - 1
        
        # initialize memory
        for i in range(0, mem_size, word_bytes):
            self.memory[i + 3] = i // self.alignment ** 3
            self.memory[i + 2] = i // self.alignment ** 2
            self.memory[i + 1] = i // self.alignment
            self.memory[i] = i % self.alignment

        # data structures
        self.num_blocks_per_set = k
        self.cache_size = cache_size
        self.block_size = block_size

        self.num_sets = (self.cache_size // (self.block_size * self.num_blocks_per_set))

        # cache bits calculation
        self.index_bits = int(math.log2(self.num_sets))
        self.block_offset_bits = int(math.log2(self.block_size))
        self.tag_bits = self.address_size - self.index_bits - self.block_offset_bits

        # assign cache
        self.cache = [[CacheBlock(self.block_size) for _ in range(self.num_blocks_per_set)] for _ in range(self.num_sets)]
        self.lru = [deque() for _ in range(self.num_sets)] 

        with open(self.file_name, "a") as out:  
            out.write("-----------------------------------------\n")
            out.write(f"cache size = {self.cache_size}\n")
            out.write(f"block size = {self.block_size}\n")                         
            out.write(f"#blocks = {self.cache_size // self.block_size}\n")
            out.write(f"#sets = {self.num_sets}\n")
            out.write(f"associativity = {self.num_blocks_per_set}\n")
            out.write(f"tag length = {self.tag_bits}\n")
            out.write("-----------------------------------------\n\n")         

    def decode_address(self, A):
        # change A to binary code in string
        address_binary = bin(A)[2:].zfill(self.address_size)

        tag = int(address_binary[:self.tag_bits], 2)  
        index = int(address_binary[self.tag_bits:self.tag_bits + self.index_bits], 2) 
        block_offset = int(address_binary[self.tag_bits + self.index_bits:], 2)  

        return [tag, index, block_offset]
    
    def read_word(self, A):
        tag, index, block_offset = self.decode_address(A)

        # collect cache
        cache_set = self.cache[index]
        lru_order = self.lru[index]

        block_index = -1
        cache_block = None

        for i, block in enumerate(cache_set):
            if block.tag == tag:
                cache_block = block
                block_index = i 
                break
        
        # Calculating upper and lower bound of the address
        lower = (A >> self.block_offset_bits) << self.block_offset_bits
        upper = lower | (2 ** self.block_offset_bits) - 1

        if cache_block:
            with open(self.file_name, "a") as out:  
                out.write(f"read hit [addr={A} index={index} block_index={block_index} tag={tag}: word={A} ({lower} - {upper})]\n")

            
            # assess which one is accessed least recent
            lru_order.remove(block_index)
            lru_order.append(block_index)
        else:
            
            # read miss, and still have space in a set
            if len(lru_order) != self.num_blocks_per_set:
                with open(self.file_name, "a") as out:  
                    out.write(f"read miss [addr={A} index={index} block_index={len(lru_order)} tag={tag}: word={A} ({lower} - {upper})]\n")
                block_index = len(lru_order)

            # read miss, and do not have space in a set
            elif len(lru_order) == self.num_blocks_per_set:

                block_index = lru_order.popleft()
                with open(self.file_name, "a") as out:  
                    out.write(f"read miss + replace [addr={A} index={index} tag={tag}: word={A} ({lower} - {upper})]\n")
                    out.write(f"evict tag {tag} in block_index {block_index}\n")
                    out.write(f"read in ({lower} - {upper})\n")
                
            self.cache[index][block_index].block = bytearray(self.memory[lower: upper + 1])
            self.cache[index][block_index].tag = tag
            cache_block = self.cache[index][block_index]

            # add it in queue
            lru_order.append(block_index)
            
        # take chunk of 4 bytes
        word_start = block_offset 
        word_data = cache_block.block[word_start : word_start + self.word_bytes]

        # calculate word
        word = 0
        for i in range(self.word_bytes):
            word += word_data[i] * (self.alignment ** i)

        return word
    def print_result(self, val):
        with open(self.file_name, "a") as out:  
            out.write(f"=> address = {val} <{bin(val)[2:].zfill(NUM_BLOCKS)}>; word = {val}\n")

cache = DMCache()

addresses = [0,0, 60, 64, 1000, 1028, 12920, 12924, 12928]
address_index = 0
while  address_index < len(addresses):
    val = cache.read_word(addresses[address_index])
    cache.print_result(val)
    address_index += 1
