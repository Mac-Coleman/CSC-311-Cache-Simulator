
from address_generator import AddressGenerator, AddressTraceGenerator
from cache import Cache, DirectCache, AssociativeCache, SetAssociativeCache, is_power_of_two
from output_builder import OutputBuilder
import ansi_terminal as cursor
from cli_parser import OptionDict

import time
import math
import sys

def simulate(options: OptionDict):
    cache: Cache | None = None

    try:
        match options["cache_type"]:
            case "direct":
                cache = DirectCache(options["block_size"], options["cache_size"], options["memory_size"])
            case "associative":
                cache = AssociativeCache(options["block_size"], options["cache_size"], options["memory_size"], options["replacement"])
            case "set-associative":
                cache = SetAssociativeCache(options["block_size"], options["cache_size"], options["memory_size"], options["replacement"], options["k"])
            case _:
                raise KeyError(f"No such cache type: {options['cache_type']}")
    except ValueError as e:
        cursor.red()
        print(f"Error", end="")
        cursor.reset()
        print(": ", end="")
        print(e)
        sys.exit(1)
    except KeyError as e:
        cursor.red()
        print(f"Error", end="")
        cursor.reset()
        print(": ", end="")
        print(e)
        sys.exit(1)

    address_maker = None

    try:
        match options["access_pattern"]:
            case "random":
                address_maker = AddressGenerator(options["memory_size"], options["block_size"], 0)
            case "random-pages":
                address_maker = AddressGenerator(options["memory_size"], options["block_size"], 1)
            case "full-sequential":
                address_maker = AddressGenerator(options["memory_size"], options["block_size"], 3)
            case _:
                address_maker = AddressTraceGenerator(options["access_pattern"], options["memory_size"], True, options["reads"])
    except FileNotFoundError:
        print(f"Error: The file {options['access_pattern']} could not be found!")
        sys.exit(1)



    output_builder = OutputBuilder()
    hit_counter = 0
    total_counter = 0

    address_length = math.ceil(math.log(options["memory_size"], 16))
    page_length = math.ceil(math.log(options["memory_size"] // options["block_size"], 16))

    locality: dict[int, int] = {}
    reads = options["reads"]

    print("\n\n")

    start = time.perf_counter()

    for i in range(options["reads"]):

        try:
            address = address_maker.generate_address()
        except StopIteration:
            break

        page, hit = cache.read(address, i)
        #output_builder.add(i, hit)
        locality[page] = locality.get(page, 0) + 1

        hit_counter += int(hit)
        total_counter += 1

        if i % 32768 == 0:
            cursor.move_up()
            cursor.move_up()
            cursor.erase()
            print("\rA: {a:0{width}x}\t  ".format(a=address, width=address_length), end="")
            cursor.green() if hit else cursor.red()
            print(f"{'hit ' if hit else 'miss'}", end="")
            cursor.reset()
            print(f"\thit ratio: {hit_counter/total_counter * 100 :0.2f}%")

            cursor.erase()
            print("[", end="")
            cursor.yellow()
            print(f"{'='*math.ceil(i/reads * 20)}{' '*math.floor((1 - (i/reads)) * 20)}", end="")
            cursor.reset()
            print(f"] Progress: {i/reads * 100:0.2f}%", end="\n")
    
    end = time.perf_counter()
    
    cursor.move_up()
    cursor.move_up()
    cursor.erase()
    print("\rA: {a:0{width}x}\t  ".format(a=address, width=address_length), end="")
    cursor.green() if hit else cursor.red()
    print(f"{'hit ' if hit else 'miss'}", end="")
    cursor.reset()
    print(f"\thit ratio: {hit_counter/total_counter * 100 :0.2f}%")
    
    cursor.erase()
    print("[", end="")
    cursor.green()
    print(f"{'='*20}", end="")
    cursor.reset()
    print(f"] Progress: Finished!", end="\n")

    hit_ratio = hit_counter / total_counter
    replacements = cache.get_replacement_count()

    print("\n  RESULTS")
    print("\t   Hit Ratio:    ", end="")
    cursor.blue()
    print(f"{hit_ratio * 100:06f} %")
    cursor.reset()
    print("\t        Hits:    ", end="")
    cursor.blue()
    print(hit_counter)
    cursor.reset()
    print("\t      Misses:    ", end="")
    cursor.blue()
    print(total_counter-hit_counter)
    cursor.reset()
    print("\t    Accesses:    ", end="")
    cursor.blue()
    print(total_counter)
    cursor.reset()
    print("\tReplacements:    ", end="")
    cursor.blue()
    print(replacements)
    cursor.reset()
    print("\t        Time:   ", end="")
    cursor.blue()
    print(f"{end-start : .02f} seconds")
    cursor.reset()
    print("\t        Rate:   ", end="")
    cursor.blue()
    print(f"{total_counter / (end-start) : .02f} accesses per second")
    cursor.reset()

    output_builder.close_output()
    output_builder.write_locality_file(locality, page_length)
    output_builder.write_stats_file(hit_counter, total_counter, replacements)