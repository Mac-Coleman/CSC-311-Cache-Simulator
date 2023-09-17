
from address_generator import AddressGenerator
from cache import Cache, DirectCache, AssociativeCache, SetAssociativeCache
from output_builder import OutputBuilder
import ansi_terminal as cursor
import sys

import time
import math

def simulate(max_size:int, page_size:int, cache_size:int, set_size:int, reads:int, replacement_algorithm: str):
    if not is_power_of_two(max_size):
        print("Memory size must be a power of two!")
        sys.exit(1)    
    if not is_power_of_two(page_size):
        print("Page size must be a power of two!")
        sys.exit(1)    
    if not is_power_of_two(cache_size):
        print("Cache size must be a power of two!")
        sys.exit(1)
    if not is_power_of_two(set_size):
        print("Set size must be a power of two!")
        sys.exit(1)

    cache = SetAssociativeCache(page_size, cache_size, max_size, "lru", set_size)
    output_builder = OutputBuilder()
    hit_counter = 0
    total_counter = 0
    address_maker = AddressGenerator(max_size, page_size, 1)

    address_length = math.ceil(math.log(max_size, 16))

    start = time.perf_counter()

    print("\n")

    for i in range(reads):
        address = address_maker.generate_address()

        page, hit = cache.read(address)
        #output_builder.add(i, hit)

        hit_counter += int(hit)
        total_counter += 1

        if i % 32768 == 0:
            cursor.move_up()
            cursor.move_up()
            cursor.erase()
            print("\rA: {a:0{width}x}\t".format(a=address, width=address_length), end="")
            cursor.green() if hit else cursor.red()
            print(f"{'hit ' if hit else 'miss'}", end="")
            cursor.reset()
            print(f"\thit ratio: {hit_counter/total_counter * 100 :0.2f}%")

            cursor.erase()
            print("[", end="")
            cursor.yellow()
            print(f"{'='*int(i/reads * 20)}{' '*int((1 - (i/reads)) * 20)}", end="")
            cursor.reset()
            print(f"] Progress: {i/reads * 100:0.2f}%", end="\n")
    
    cursor.move_up()
    cursor.move_up()
    cursor.erase()
    print("\rA: {a:0{width}x}\t".format(a=address, width=address_length), end="")
    cursor.green() if hit else cursor.red()
    print(f"{'hit ' if hit else 'miss'}", end="")
    cursor.reset()
    print(f"\thit ratio: {hit_counter/total_counter * 100 :0.2f}%")
    
    cursor.erase()
    print("[", end="")
    cursor.green()
    print(f"{'='*int(i/reads * 20)}{' '*int((1 - (i/reads)) * 20)}", end="")
    cursor.reset()
    print(f"] Progress: Finished!", end="\n")

    hit_ratio = hit_counter / total_counter
    replacements = cache.get_replacement_count()
    output_builder.close_output()
    output_builder.print_data(hit_ratio, replacements, 0)
    #output builder make output from replacements and hit record 
def is_power_of_two(num: int) -> bool:
    # For any power of two, its binary interpretation can have exactly one set bit.
    return num.bit_count() == 1