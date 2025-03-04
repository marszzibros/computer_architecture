from cache_simulator import CacheBlock, Cache

BITS_PER_BYTE = 8
WORD_BYTES = 4
MEM_SIZE = 64000
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
                address_size = 16)

addresses = [1152, 2176, 3200, 4224, 5248, 7296]
address_index = 0
while  address_index < len(addresses):
    val = cache.read_word(addresses[address_index])
    cache.print_result(val)
    address_index += 1
