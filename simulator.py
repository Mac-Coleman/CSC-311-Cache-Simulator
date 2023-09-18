
from address_generator import AddressGenerator
from cache import Cache, DirectCache, AssociativeCache, SetAssociativeCache
from output_builder import OutputBuilder
import ansi_terminal as cursor

import time
import math

def simulate(max_size:int, page_size:int, cache_size:int, set_size:int, reads:int, replacement_algorithm: str):
    cache = SetAssociativeCache(page_size, cache_size, max_size, "lru", set_size)
    output_builder = OutputBuilder()
    hit_counter = 0
    total_counter = 0
    address_maker = AddressGenerator(max_size, page_size, 0)
    address_length = math.ceil(math.log(max_size, 16))
    page_length = math.ceil(math.log(max_size // page_size, 16))

    locality: dict[int, int] = {}
    start = time.perf_counter()

    print("\n")

    for i in range(reads):
        address = address_maker.generate_address()

        page, hit = cache.read(address)
        #output_builder.add(i, hit)
        locality[page] = locality.get(page, 0) + 1

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
            print(f"{'='*math.floor(i/reads * 20)}{' '*math.ceil((1 - (i/reads)) * 20)}", end="")
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
    print(f"{'='*math.floor(i/reads * 20)}{' '*math.ceil((1 - (i/reads)) * 20)}", end="")
    cursor.reset()
    print(f"] Progress: Finished!", end="\n")

    hit_ratio = hit_counter / total_counter
    replacements = cache.get_replacement_count()
    output_builder.close_output()
    output_builder.print_data(hit_ratio, replacements, 0)
    #output builder make output from replacements and hit record
    output_builder.write_locality_file(locality, page_length)