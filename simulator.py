
from address_generator import AddressGenerator
from cache import Cache, DirectCache, AssociativeCache
from output_builder import OutputBuilder

import time

def simulator(max_size:int, page_size:int, cache_size:int, set_size:int, reads:int, replacement_algorithm: str):
    cache = AssociativeCache(page_size, cache_size, max_size)
    output_builder = OutputBuilder()
    hit_counter = 0
    total_counter = 0
    address_maker = AddressGenerator(max_size)

    start = time.perf_counter()

    for i in range(reads):
        address = address_maker.generate_address()

        page, hit = cache.read(address)
        #output_builder.add(i, hit)

        hit_counter += int(hit)
        total_counter += 1

        if i % 1000 == 0:
            print(f"\rA: {address:016x}, hit: {hit:b}, {i/reads * 100 :.2f}%", end="")
    
    print(f"\rA: {address:016x}, hit: {hit:b}, {100:.2f}%")
    
    print(time.perf_counter() - start)

    hit_ratio = hit_counter / total_counter
    replacements = cache.get_replacement_count()
    output_builder.close_output()
    output_builder.print_data(hit_ratio, replacements, 0)
    #output builder make output from replacements and hit record 