import numpy as np
import math

from collections import deque
from enum import Enum, auto

class AccessType(Enum):
    READ:str = "read"
    WRITE:str = "write"

class CacheBlock:
    def __init__(self, size):
        # integer tag
        self.tag = -1

        # data block bytearray
        self.block = bytearray(size)
        
        # dirty - False, clean - True
        self.dirty_flag = False

        # invalid - False, valid - True
        self.valid_flag = False

class Cache:
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
        self.associativity = k
        self.cache_size = cache_size
        self.block_size = block_size

        self.num_sets = (self.cache_size // (self.block_size * self.associativity))

        # cache bits calculation
        self.index_bits = int(math.log2(self.num_sets))
        self.block_offset_bits = int(math.log2(self.block_size))
        self.tag_bits = self.address_size - self.index_bits - self.block_offset_bits

        # assign cache
        self.cache = [[CacheBlock(self.block_size) for _ in range(self.associativity)] for _ in range(self.num_sets)]
        self.lru = [deque([-1] * self.associativity) for _ in range(self.num_sets)]

        with open(self.file_name, "a") as out:  
            out.write("-----------------------------------------\n")
            out.write(f"cache size = {self.cache_size}\n")
            out.write(f"block size = {self.block_size}\n")                         
            out.write(f"#blocks = {self.cache_size // self.block_size}\n")
            out.write(f"#sets = {self.num_sets}\n")
            out.write(f"associativity = {self.associativity}\n")
            out.write(f"tag length = {self.tag_bits}\n")
            out.write("-----------------------------------------\n\n")         

    def decode_address(self, A):
        # change A to binary code in string
        address_binary = bin(A)[2:].zfill(self.address_size)

        tag = int(address_binary[:self.tag_bits], 2)  
        index = int(address_binary[self.tag_bits:self.tag_bits + self.index_bits], 2) 
        block_offset = int(address_binary[self.tag_bits + self.index_bits:], 2)  

        return [tag, index, block_offset]
    
    def access_memory(self, address, word, access_type):

        hit = False
        miss_have_space = False
        miss_no_space = False

        tag, index, block_offset = self.decode_address(address)

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
        lower = (address >> self.block_offset_bits) << self.block_offset_bits
        upper = lower | (2 ** self.block_offset_bits) - 1

        if word is None:
            word = address

        if cache_block:
            hit = True

            # assess which one is accessed least recent
            lru_order.remove(block_index)
            lru_order.append(block_index)
        else:
            # read miss, and still have space in a set
            if lru_order.count(-1) > 0:
                block_index = self.associativity - lru_order.count(-1)
                lru_order.popleft()

                miss_have_space = True
                
            # read miss, and do not have space in a set
            elif lru_order.count(-1) == 0:
                block_index = lru_order.popleft()
                miss_no_space = True
            self.cache[index][block_index].block = bytearray(self.memory[lower: upper + 1])
            self.cache[index][block_index].tag = tag
            self.cache[index][block_index].dirty_flag = True
            self.cache[index][block_index].valid_flag = True

            cache_block = self.cache[index][block_index]

            # add it in queue
            lru_order.append(block_index)

        # take chunk of 4 bytes
        word_start = block_offset 
        word_data = cache_block.block[word_start : word_start + self.word_bytes]
        cache_block.dirty_flag = False



        if access_type == AccessType.READ:
            # calculate word
            word = 0
            for i in range(self.word_bytes):
                word += word_data[i] * (self.alignment ** i)
                  
        elif access_type == AccessType.WRITE:
            for i in range(self.word_bytes - 1, -1, -1):
                word_data[i] = word // (self.alignment ** i)
                word %= self.alignment ** i

            memory_address = (tag << (self.index_bits + self.block_offset_bits)) | (index << self.block_offset_bits) | block_offset
            for i in range(self.word_bytes):
                self.memory[memory_address + i] = word_data[i]

        if hit:
            with open(self.file_name, "a") as out:  
                out.write(f"{access_type.value} hit [addr={address} index={index} block_index={block_index} tag={tag}: word={word} ({lower} - {upper})]\n")
        elif miss_have_space:
            with open(self.file_name, "a") as out:  
                out.write(f"{access_type.value} miss [addr={address} index={index} block_index={block_index} tag={tag}: word={word} ({lower} - {upper})]\n")
        elif miss_no_space:
            with open(self.file_name, "a") as out:  
                out.write(f"{access_type.value} miss + replace [addr={address} index={index} tag={tag}: word={word} ({lower} - {upper})]\n")
                out.write(f"evict tag {self.cache[index][block_index].tag} in block_index {block_index}\n")
                out.write(f"{access_type.value} in ({lower} - {upper})\n")
        
        with open(self.file_name, "a") as out:
            out.write("[ ")
            for item in lru_order:
                out.write(f"{self.cache[index][item].tag} ")
            out.write("]\n")

        if access_type == AccessType.READ:
            return word  
        
    def read_word(self, A):
        return self.access_memory(A, None, access_type=AccessType.READ)
    def write_word(self, A, word):
        self.access_memory(A, word, access_type=AccessType.WRITE)
    def print_result(self, val):
        num_blocks = (self.cache_size // self.block_size)
        with open(self.file_name, "a") as out:  
            out.write(f"address = {val} <{bin(val)[2:].zfill(num_blocks)}>; word = {val}\n\n")

