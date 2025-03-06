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
                    cache_size = 131072,
                    block_size = 64,
                    address_size = 48, mode = mode,file_name=f"output/cholesky-instruction-accesses-{mode}.out",use_memory=False, debug=False)


    cache.process_trace(filename = os.path.join(file_dir, "cholesky-full-run.atrace.out"), trace_mode ="i")

    # data mode
    cache = Cache(mem_size = MEM_SIZE,
                    word_bytes = WORD_BYTES,
                    k = 4,
                    cache_size = 131072,
                    block_size = 64,
                    address_size = 48, mode ="wb",file_name=f"output/cholesky-data-accesses-{mode}.out",use_memory=False, debug=False)


    cache.process_trace(filename = os.path.join(file_dir, "cholesky-full-run.atrace.out"), trace_mode ="d")


    # instruction mode
    cache = Cache(mem_size = MEM_SIZE,
                    word_bytes = WORD_BYTES,
                    k = 4,
                    cache_size = 131072,
                    block_size = 64,
                    address_size = 48, mode ="wb",file_name=f"output/curl-instruction-accesses-{mode}.out",use_memory=False, debug=False)

    cache.process_trace(filename = os.path.join(file_dir, "curl-portion.atrace.out"), trace_mode ="i")

    # data mode
    cache = Cache(mem_size = MEM_SIZE,
                    word_bytes = WORD_BYTES,
                    k = 4,
                    cache_size = 131072,
                    block_size = 64,
                    address_size = 48, mode ="wb",file_name=f"output/curl-data-accesses-{mode}.out",use_memory=False, debug=False)

    cache.process_trace(filename = os.path.join(file_dir, "curl-portion.atrace.out"), trace_mode ="d")


    # instruction mode
    cache = Cache(mem_size = MEM_SIZE,
                    word_bytes = WORD_BYTES,
                    k = 4,
                    cache_size = 131072,
                    block_size = 64,
                    address_size = 48, mode ="wb",file_name=f"output/rand-instruction-accesses-{mode}.out",use_memory=False, debug=False)

    cache.process_trace(filename = os.path.join(file_dir, "rand-data-accesses.atrace.out"), trace_mode ="i")

    # data mode
    cache = Cache(mem_size = MEM_SIZE,
                    word_bytes = WORD_BYTES,
                    k = 4,
                    cache_size = 131072,
                    block_size = 64,
                    address_size = 48, mode ="wb",file_name=f"output/rand-data-accesses-{mode}.out",use_memory=False, debug=False)

    cache.process_trace(filename = os.path.join(file_dir, "rand-data-accesses.atrace.out"), trace_mode ="d")
