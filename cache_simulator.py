"""
The top-level organization for the main program logic.
This will orchestrate the simulator and its components.
"""

from cli_parser import parse_arguments
from cache import Cache
from simulator import simulate

import sys
import random
import time

program_name = "CacheSim"
version = "0.0.1"

# fdisk is a good example of a help message.
help_string = f"\n{program_name} {version}\n\n" \
    "Usage:\n" \
    "  python {executing_file_name} [options] <cache-type> <reads>\n\n" \
    "Simulate reads and writes to a cache.\n\n" \
    "Options:\n" \
    " -b, --block-size <size>  block, page, frame, line size\n" \
    "                          default: 4KB\n" \
    " -c, --cache-size <size>  size of the cache\n" \
    "                          default: 32KB\n" \
    " -h, --help               display this help message\n" \
    " -k, --ways <set-size>    the size of each set in a set-associative cache\n" \
    " -m, --memory-size <size> physical memory size\n" \
    "                          default: 256MB\n" \
    " -v, --version            display version\n" \
    

def main():
    parse_arguments(sys.argv, run_help, run_version, run_simulator)

def run_version(executing_file: str):
    print(f"{program_name} {version}")

def run_help(executing_file: str):
    print(help_string.format(executing_file_name=executing_file))

def run_simulator(options: dict[str, int]):
    simulate(options["memory_size"], options["block_size"], options["cache_size"], options["k"], options["reads"], "lru")



if __name__ == "__main__":
    main()