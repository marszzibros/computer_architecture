from cache_simulator import Cache
import argparse


BITS_PER_BYTE = 8
WORD_BYTES = 4
MEM_SIZE = 640000000
CACHE_BLOCKS = 2 ** 10
CACHE_PER_BLOCK = 2 ** 6
NUM_BLOCKS = CACHE_BLOCKS // CACHE_PER_BLOCK

# Since it is direct-mapped cache 
NUM_WAYS = 4
NUM_SETS  = NUM_BLOCKS // NUM_WAYS


cache = Cache(mem_size = MEM_SIZE,
                word_bytes = WORD_BYTES,
                k = NUM_WAYS,
                cache_size = CACHE_BLOCKS,
                block_size = CACHE_PER_BLOCK,
                address_size = 16, 
                mode ="wb",
                file_name="part-two-three.out",
                use_memory=True)

i_cache = Cache(mem_size = MEM_SIZE,
                word_bytes = WORD_BYTES,
                k = 4,
                cache_size = 2048,
                block_size = 64,
                address_size = 48, mode ="wb",file_name="rand-instruction-accesses.out",use_memory=False)
d_cache = Cache(mem_size = MEM_SIZE,
                word_bytes = WORD_BYTES,
                k = 4,
                cache_size = 2048,
                block_size = 64,
                address_size = 48, mode ="wb",file_name="rand-data-accesses.out",use_memory=False)
i_cache.process_trace(filename = "forstudents_s25/CS3220/CacheSim/cholesky-full-run.atrace.out", trace_mode ="i")


# with open("part-two-three-addresses.txt", "r") as file_input:
#     for row in file_input.readlines():
#         row = row.rstrip("\n")
#         if "read_word" in row:
#             row = row.lstrip("read_word(").rstrip(")")
#             val = cache.read_word(int(row))
#         elif "write_word" in row:
#             row = row.lstrip("write_word(").rstrip(")")
#             row_value = row.split(", ")
#             val = cache.write_word(int(row_value[0]), int(row_value[1]))