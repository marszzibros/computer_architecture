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
        
        # dirty - True, clean - False
        self.dirty_flag = False

        # invalid - False, valid - True
        self.valid_flag = False

class Cache:
    def __init__(self, mem_size = 64000, 
                 word_bytes = 4, 
                 k = 1, 
                 cache_size = 2 ** 10, 
                 block_size = 2 ** 6, 
                 address_size = 16, 
                 mode = "wt", 
                 file_name = "part-one-test.out",
                 use_memory = True,
                 debug = False):
        self.file_name = file_name
        self.memory = np.zeros(mem_size, dtype=np.uint8)
        self.address_size = address_size
        self.word_bytes = word_bytes
        self.alignment = 256
        self.mode = mode
        self.use_memory = use_memory

        self.reads = 0
        self.read_hits = 0
        self.writes = 0
        self.write_hits = 0  
        self.mem_size = mem_size
        self.debug = debug

        # define m
        m = mem_size / 4 - 1
        
        # initialize memory
        if self.use_memory:
            self.memory = np.zeros(mem_size, dtype=np.uint8)
            indices = np.arange(0, mem_size, word_bytes, dtype=np.uint32)
            self.memory[0::4] = indices % 256
            self.memory[1::4] = (indices // 256) % 256
            self.memory[2::4] = (indices // 256**2) % 256
            self.memory[3::4] = indices // 256**3
        else:
            self.memory = None

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
        self.lru_tag = [deque([-1] * self.associativity) for _ in range(self.num_sets)]

        if use_memory:
            with open(self.file_name, "a") as out:  
                out.write("-----------------------------------------\n")
                out.write(f"cache size = {self.cache_size}\n")
                out.write(f"block size = {self.block_size}\n")                         
                out.write(f"#blocks = {self.cache_size // self.block_size}\n")
                out.write(f"#sets = {self.num_sets}\n")
                out.write(f"associativity = {self.associativity}\n")
                out.write(f"memory_size_bits = {2 ** self.word_bytes}\n")
                out.write(f"tag length = {self.tag_bits}\n")
                if mode == "wt":
                    out.write(f"write through\n")
                elif mode == "wb":
                    out.write(f"write back\n")
                out.write("-----------------------------------------\n\n")         

    def decode_address(self, A):
        tag = A >> (self.index_bits + self.block_offset_bits)

        # index is the set number
        index = (A // self.block_size) & (self.num_sets - 1)
        # offset in block is lowest bits
        block_offset = A & (self.block_size - 1)

        return [tag, index, block_offset]

    
    def access_memory(self, address, word, access_type):

        hit = False
        miss_have_space = False
        miss_no_space = False

        tag, index, block_offset = self.decode_address(address)
        if block_offset % 4 == 0 and address >= 0 and (not self.use_memory or address < self.mem_size) :

            # collect cache
            cache_set = self.cache[index]
            lru_order = self.lru[index]
            lru_tag_q = self.lru_tag[index]

            block_index = -1
            cache_block = None

            write_back = False

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

                lru_tag_q.remove(tag)
                lru_tag_q.append(tag)            
            else:
                # read miss, and still have space in a set
                if lru_order.count(-1) > 0:
                    block_index = self.associativity - lru_order.count(-1)
                    lru_order.popleft()
                    lru_tag_q.popleft()

                    miss_have_space = True
                    
                # read miss, and do not have space in a set
                elif lru_order.count(-1) == 0:
                    block_index = lru_order.popleft()
                    prv_tag = lru_tag_q.popleft()
                    miss_no_space = True
                    

                    evicted_block = self.cache[index][block_index]

                    if evicted_block.dirty_flag and self.mode == "wb":
                        evicted_address = (prv_tag << (self.index_bits + self.block_offset_bits)) | (index << self.block_offset_bits)
                        
                        lower_evi = evicted_address
                        upper_evi = lower_evi | (2 ** self.block_offset_bits) - 1
                        if self.use_memory:
                            self.memory[lower_evi: upper_evi + 1] = evicted_block.block 

                        write_back = True

                if self.use_memory:
                    self.cache[index][block_index].block = bytearray(self.memory[lower: upper + 1])
                else:
                    self.cache[index][block_index].block = bytearray(self.block_size)
                self.cache[index][block_index].tag = tag
                self.cache[index][block_index].valid_flag = True

                cache_block = self.cache[index][block_index]

                # add it in queue
                lru_order.append(block_index)
                lru_tag_q.append(tag)

            # take chunk of 4 bytes
            word_data = cache_block.block[block_offset : block_offset + self.word_bytes]

            if access_type == AccessType.READ:
                self.reads += 1
                if hit:
                    self.read_hits += 1
            else:  # WRITE
                self.writes += 1
                if hit:
                    self.write_hits += 1


            if access_type == AccessType.READ:
                # calculate word
                word = 0
                if self.use_memory:
                    for i in range(self.word_bytes):
                        word += word_data[i] * (self.alignment ** i)
                    
            elif access_type == AccessType.WRITE:
                

                if self.mode == "wt":
                    word_temp = word
                    for i in range(self.word_bytes - 1, -1, -1):
                        cache_block.block[block_offset + i] = word_temp // (self.alignment ** i)
                        word_temp %= self.alignment ** i
                    if self.use_memory:
                        for i in range(self.word_bytes):
                            self.memory[address + i] = cache_block.block[block_offset + i]

                elif self.mode == "wb":
                    word_temp = word

                    for i in range(self.word_bytes - 1, -1, -1):

                        cache_block.block[block_offset + i] = word_temp // (self.alignment ** i)

                        word_temp %= self.alignment ** i

                    cache_block.dirty_flag = True
            if self.debug:
                if hit:
                    with open(self.file_name, "a") as out:  
                        out.write(f"{access_type.value} hit [addr={address} index={index} block_index={block_index} tag={tag}: word={word} ({lower} - {upper})]\n")
                elif miss_have_space:
                    with open(self.file_name, "a") as out:  
                        out.write(f"{access_type.value} miss [addr={address} index={index} block_index={block_index} tag={tag}: word={word} ({lower} - {upper})]\n")
                elif miss_no_space:
                    with open(self.file_name, "a") as out:  
                        out.write(f"{access_type.value} miss + replace [addr={address} index={index} tag={tag}: word={word} ({lower} - {upper})]\n")
                        out.write(f"evict tag {prv_tag} in block_index {block_index}\n")
                        if self.mode == "wb" and write_back:
                            out.write(f"write back ({lower_evi} - {upper_evi})\n")
                            write_back = False
                        
                        out.write(f"read in ({lower} - {upper})\n")


                with open(self.file_name, "a") as out:
                    out.write("[ ")
                    for item in lru_tag_q:
                        out.write(f"{item} ")
                    out.write("]\n")
                    if access_type == AccessType.READ:
                        out.write(f"address = {address}; word = {word}\n\n")
                    else:
                        out.write(f"\n")
                    if self.mode == "wt":            
                        out.write(f"write through: write {word} to mem[{block_offset}]\n")        
            if access_type == AccessType.READ:
                return word  
        else:

            with open("log.txt", "a") as write_file:
                write_file.write(f"{hex(address)} is not in range!\n")
        
    def read_word(self, A):
        return self.access_memory(A, None, access_type=AccessType.READ)
    def write_word(self, A, word):
        self.access_memory(A, word, access_type=AccessType.WRITE)

    def process_trace(self, filename, trace_mode="i"):
        with open(filename, "r") as f:
            for line in f:
                parts = line.strip().split()
                if "#eof" in parts:
                    break
                if trace_mode == "i":
                    if len(parts) == 1: 
                        addr = int(parts[0], 16) 
                        self.read_word(addr)
                else:
                    if len(parts) == 3:
                        op = parts[1]
                        data_addr = int(parts[2], 16)
                        if op == "R":
                            self.read_word(data_addr)
                        elif op == "W":
                            self.write_word(data_addr, 0) 

        with open(self.file_name, "a") as out:
            out.write(f"cache size = {self.cache_size}\n")
            out.write(f"cache block size = {self.block_size}\n")
            out.write(f"cache #blocks = {self.cache_size // self.block_size}\n")
            out.write(f"cache #sets = {self.num_sets}\n")
            out.write(f"cache associativity = {self.associativity}\n")
            out.write(f"cache tag length = {self.tag_bits}\n")
            out.write(f"{'write back' if self.mode == 'wb' else 'write through'}\n")
            if self.reads > 0:
                out.write(f"# reads = {self.reads}\n")
                read_misses = self.reads - self.read_hits
                out.write(f"# read misses = {read_misses} ({read_misses/self.reads*100:.2f}%)\n")
                out.write(f"# read hits = {self.read_hits} ({self.read_hits/self.reads*100:.2f}%)\n")
            if self.writes > 0:
                out.write(f"# writes = {self.writes}\n")
                write_misses = self.writes - self.write_hits
                out.write(f"# write misses = {write_misses} ({write_misses/self.writes*100:.2f}%)\n")
                out.write(f"# write hits = {self.write_hits} ({self.write_hits/self.writes*100:.2f}%)\n")
    