"""
The top-level organization for the main program logic.
This will orchestrate the simulator and its components.
"""

from cli_parser import parse_arguments, OptionDict
from cache import Cache
from simulator import simulate
import ansi_terminal as cursor

import sys
import random
import time
from typing import cast

program_name = "CacheSim"
version = "0.0.1"

# fdisk is a good example of a help message.
help_string = f"\n{program_name} {version}\n\n" \
    "Usage:\n" \
    "  python {executing_file_name} [options] <cache-type> <reads>\n\n" \
    "Simulate reads and writes to a cache.\n\n" \
    "Options:\n" \
    " -a, --access-pattern <pattern>  the access pattern to use\n" \
    " -b, --block-size <size>         block, page, frame, line size\n" \
    "                                 default: 4KB\n" \
    " -c, --cache-size <size>         size of the cache\n" \
    "                                 default: 32KB\n" \
    " -h, --help                      display this help message\n" \
    " -k, --ways <set-size>           the size of each set in a set-associative cache\n" \
    " -m, --memory-size <size>        physical memory size\n" \
    "                                 default: 256MB\n" \
    " -n, --no-color                  disable colored output\n" \
    " -q, --quiet                     suppress progress display\n" \
    " -p, --probability               set probability of next address being generated\n" \
    "                                 in a new page than the previous address.\n" \
    "                                 default: 2" \
    " -r, --replacement <algorithm>   replacement algorithm to use in caches with associativity\n" \
    "                                 default: least recently used\n" \
    " -v, --version                   display version\n" \
    

def main():
    parse_arguments(sys.argv, run_help, run_version, run_simulator)

def run_version(executing_file: str):
    print(f"{program_name} {version}")

def run_help(executing_file: str):
    print(help_string.format(executing_file_name=executing_file))

def run_simulator(options: OptionDict):
    try:
        cursor.setup(cast(bool, options["no_color"]))
        simulate(options)
    except KeyboardInterrupt:
        cursor.erase()
        cursor.red()
        print("Simulation canceled!")
        cursor.reset()



if __name__ == "__main__":
    main()