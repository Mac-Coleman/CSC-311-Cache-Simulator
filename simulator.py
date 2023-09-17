
from address_generator import AddressGenerator
from cache import Cache, DirectCache, AssociativeCache, SetAssociativeCache
from output_builder import OutputBuilder

import ansi_terminal as cursor

import time

def simulate(max_size:int, page_size:int, cache_size:int, set_size:int, reads:int, replacement_algorithm: str):
    cache = SetAssociativeCache(page_size, cache_size, max_size, "lru", set_size)
    output_builder = OutputBuilder()
    hit_counter = 0
    total_counter = 0
    address_maker = AddressGenerator(max_size)

    start = time.perf_counter()

    print("\n")

    for i in range(reads):
        address = address_maker.generate_address()

        page, hit = cache.read(address)
        #output_builder.add(i, hit)

        hit_counter += int(hit)
        total_counter += 1

        if i % 1000 == 0:
            cursor.move_up()
            cursor.move_up()
            cursor.erase()
            print(f"\rA: {address:016x}, hit: ", end="")
            cursor.green() if hit else cursor.red()
            print(f"{hit:b}", end="")
            cursor.reset()
            print(f", hit ratio: {hit_counter/total_counter * 100 :0.2f}%")
            
            cursor.yellow()
            cursor.erase()
            print(f"[{'='*int(i/reads * 20)}{' '*int((1 - (i/reads)) * 20)}] Progress: {i/reads * 100:0.2f}%", end="\n")
            cursor.reset()
    
    cursor.move_up()
    cursor.move_up()
    cursor.erase()
    print(f"\rA: {address:016x}, hit: ", end="")
    cursor.green() if hit else cursor.red()
    print(f"{hit:b}", end="")
    cursor.reset()
    print(f", hit ratio: {hit_counter/total_counter * 100 :0.2f}%")
    
    cursor.green()
    cursor.erase()
    print(f"[{'='*int(i/reads * 20)}{' '*int((1 - (i/reads)) * 20)}] Progress: {i/reads * 100:0.2f}%", end="\n")
    cursor.reset()

    hit_ratio = hit_counter / total_counter
    replacements = cache.get_replacement_count()
    output_builder.close_output()
    output_builder.print_data(hit_ratio, replacements, 0)
    #output builder make output from replacements and hit record 