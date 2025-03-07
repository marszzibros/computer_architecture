from cache_simulator import Cache
import os

BITS_PER_BYTE = 8
WORD_BYTES = 4
# 16 GB
MEM_SIZE = 64000
CACHE_BLOCKS = 2 ** 10
CACHE_PER_BLOCK = 2 ** 6
NUM_BLOCKS = CACHE_BLOCKS // CACHE_PER_BLOCK

# Since it is direct-mapped cache 
NUM_WAYS = 4
NUM_SETS  = NUM_BLOCKS // NUM_WAYS

with open("log.txt", "w") as reset:
    pass 

file_dir = "input"

for mode in ["wb", "wt"]:

    cache = Cache(mem_size = MEM_SIZE,
                    word_bytes = WORD_BYTES,
                    k = NUM_WAYS,
                    cache_size = CACHE_BLOCKS,
                    block_size = CACHE_PER_BLOCK,
                    address_size = 16, 
                    mode = mode,
                    file_name=f"output/part-two-one-{mode}.out",
                    use_memory=True,debug=True)


    with open("input/part-two-one-addresses.txt", "r") as file_input:
        for row in file_input.readlines():
            row = row.rstrip("\n")
            if "read_word" in row:
                row = row.lstrip("read_word(").rstrip(")")
                val = cache.read_word(int(row))
            elif "write_word" in row:
                row = row.lstrip("write_word(").rstrip(")")
                row_value = row.split(", ")
                val = cache.write_word(int(row_value[0]), int(row_value[1]))

    cache = Cache(mem_size = MEM_SIZE,
                    word_bytes = WORD_BYTES,
                    k = NUM_WAYS,
                    cache_size = CACHE_BLOCKS,
                    block_size = CACHE_PER_BLOCK,
                    address_size = 16, 
                    mode = mode,
                    file_name=f"output/part-two-two-{mode}.out",
                    use_memory=True,debug=True)

    with open("input/part-two-two-addresses.txt", "r") as file_input:
        for row in file_input.readlines():
            row = row.rstrip("\n")
            if "read_word" in row:
                row = row.lstrip("read_word(").rstrip(")")
                val = cache.read_word(int(row))
            elif "write_word" in row:
                row = row.lstrip("write_word(").rstrip(")")
                row_value = row.split(", ")
                val = cache.write_word(int(row_value[0]), int(row_value[1]))

    cache = Cache(mem_size = MEM_SIZE,
                    word_bytes = WORD_BYTES,
                    k = NUM_WAYS,
                    cache_size = CACHE_BLOCKS,
                    block_size = CACHE_PER_BLOCK,
                    address_size = 16, 
                    mode = mode,
                    file_name=f"output/part-two-three-{mode}.out",
                    use_memory=True, debug=True)


    with open("input/part-two-three-addresses.txt", "r") as file_input:
        for row in file_input.readlines():
            row = row.rstrip("\n")
            if "read_word" in row:
                row = row.lstrip("read_word(").rstrip(")")
                val = cache.read_word(int(row))
            elif "write_word" in row:
                row = row.lstrip("write_word(").rstrip(")")
                row_value = row.split(", ")
                val = cache.write_word(int(row_value[0]), int(row_value[1]))




    # instruction mode
    cache = Cache(mem_size = MEM_SIZE,
                    word_bytes = WORD_BYTES,
                    k = 4,
                    cache_size = 65536,
                    block_size = 64,
                    address_size = 48, mode = mode,file_name=f"output/cholesky-instruction-accesses-{mode}.out",use_memory=False, debug=False)


    cache.process_trace(filename = os.path.join(file_dir, "cholesky-full-run.atrace.out"), trace_mode ="i")

    # data mode
    cache = Cache(mem_size = MEM_SIZE,
                    word_bytes = WORD_BYTES,
                    k = 4,
                    cache_size = 65536,
                    block_size = 64,
                    address_size = 48, mode =mode,file_name=f"output/cholesky-data-accesses-{mode}.out",use_memory=False, debug=False)


    cache.process_trace(filename = os.path.join(file_dir, "cholesky-full-run.atrace.out"), trace_mode ="d")

    # all mode
    cache = Cache(mem_size = MEM_SIZE,
                    word_bytes = WORD_BYTES,
                    k = 4,
                    cache_size = 131072,
                    block_size = 64,
                    address_size = 48, mode =mode,file_name=f"output/cholesky-all-accesses-{mode}.out",use_memory=False, debug=False)


    cache.process_trace(filename = os.path.join(file_dir, "cholesky-full-run.atrace.out"), trace_mode ="all")

    # instruction mode
    cache = Cache(mem_size = MEM_SIZE,
                    word_bytes = WORD_BYTES,
                    k = 4,
                    cache_size = 65536,
                    block_size = 64,
                    address_size = 48, mode =mode,file_name=f"output/curl-instruction-accesses-{mode}.out",use_memory=False, debug=False)

    cache.process_trace(filename = os.path.join(file_dir, "curl-portion.atrace.out"), trace_mode ="i")

    # data mode
    cache = Cache(mem_size = MEM_SIZE,
                    word_bytes = WORD_BYTES,
                    k = 4,
                    cache_size = 65536,
                    block_size = 64,
                    address_size = 48, mode =mode,file_name=f"output/curl-data-accesses-{mode}.out",use_memory=False, debug=False)

    cache.process_trace(filename = os.path.join(file_dir, "curl-portion.atrace.out"), trace_mode ="d")

    # all mode
    cache = Cache(mem_size = MEM_SIZE,
                    word_bytes = WORD_BYTES,
                    k = 4,
                    cache_size = 131072,
                    block_size = 64,
                    address_size = 48, mode =mode,file_name=f"output/curl-all-accesses-{mode}.out",use_memory=False, debug=False)

    cache.process_trace(filename = os.path.join(file_dir, "curl-portion.atrace.out"), trace_mode ="all")

    # instruction mode
    cache = Cache(mem_size = MEM_SIZE,
                    word_bytes = WORD_BYTES,
                    k = 4,
                    cache_size = 65536,
                    block_size = 64,
                    address_size = 48, mode =mode,file_name=f"output/rand-instruction-accesses-{mode}.out",use_memory=False, debug=False)

    cache.process_trace(filename = os.path.join(file_dir, "rand-data-accesses.atrace.out"), trace_mode ="i")

    # data mode
    cache = Cache(mem_size = MEM_SIZE,
                    word_bytes = WORD_BYTES,
                    k = 4,
                    cache_size = 65536,
                    block_size = 64,
                    address_size = 48, mode =mode,file_name=f"output/rand-data-accesses-{mode}.out",use_memory=False, debug=False)

    cache.process_trace(filename = os.path.join(file_dir, "rand-data-accesses.atrace.out"), trace_mode ="d")

    # all mode
    cache = Cache(mem_size = MEM_SIZE,
                    word_bytes = WORD_BYTES,
                    k = 4,
                    cache_size = 131072,
                    block_size = 64,
                    address_size = 48, mode =mode,file_name=f"output/rand-all-accesses-{mode}.out",use_memory=False, debug=False)

    cache.process_trace(filename = os.path.join(file_dir, "rand-data-accesses.atrace.out"), trace_mode ="all")


# Below will talk about cache split for instructions and data; size will be 65536 bytes

# It appears that Cholesky (I think it is about Cholesky decomposition—did a little research)  
# is a cache-efficient method. The results show that the data read hit rate is slightly higher  
# than the instruction hit rate. I think this happens because Cholesky decomposition involves  
# matrix multiplication, which makes better use of cache locality by working on smaller  
# submatrices that fit into the cache efficiently.  

# When dealing with the Curl file, the instruction read hit rate is higher than the data  
# read hit rate. Both the read hit rate and write hit rate are high, which suggests the  
# system is managing the cache efficiently.  

# When dealing with the rand file, both the instruction read hit rate and data read hit  
# rate are very high, with the data read rate being slightly higher. However, quite notably,  
# the write hit rate in data is very low (50%), which shows that the cache is not managed  
# efficiently for writes. 


# When cache is unified (131072 bytes), this is what happened:

# Cholesky
# Reads misses in unified: 2812
# Reads misses in split: 1677 + 1230 = 2907
# Results: unified misses are lower in unified, write misses got slightly lower in unified

# Curl
# Reads misses in unified: 44784
# Reads misses in split: 56501 + 2477 = 58978
# Results: unified misses are astonishingly lower in unified, write misses got slightly lower in unified

# Rand
# Reads misses in unified: 2283
# Reads misses in split: 1395 + 912 = 2307
# Results: unified misses are slightly lower in unified, write misses got slightly lower in unified

# Final Results: The unified cache provides better overall performance compared to the split cache, 
# as it consistently lowers misses for both reads and writes across all workloads.
# I am assuming that unified cache has more room (sets) to store data/instructions to make hit rate higher.