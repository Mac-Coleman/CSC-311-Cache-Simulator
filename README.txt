CSC 311 Cache Simulator Project

Authors: Brodie McCuen, Torii Greiskalns, Mac Coleman
Block 1, 2023
Cornell College

This project provides a simulator for different types of caches.

Usage:
python cache_simulator.py <CACHE-TYPE> <READS> [options]

Optional Arguments:
  -a, --access-pattern <pattern>  the access pattern to use
                                  can be a path to a Valgrind Lackey trace file
  -b, --block-size <size>         block, page, frame, line size
                                  default: 4KB
  -c, --cache-size <size>         size of the cache
                                  default: 32KB
  -d, --disable-output-files      disables writing of output files hit_and_miss.txt,
                                  stats.txt, and locality.txt
  -h, --help                      display this help message
  -k, --ways <set-size>           the size of each set in a set-associative cache
                                  required for set-associative caches
  -m, --memory-size <size>        physical memory size
                                  default: 256MB
  -n, --no-color                  disable colored output
  -q, --quiet                     suppress progress display
  -p, --probability               set probability of next address being generated
                                  in a new page than the previous address.
  -r, --replacement <algorithm>   replacement algorithm to use in caches with associativity
                                  default: least recently used
  -v, --version                   display version

Supported Cache Types:
    direct            map each page to a specific cache line
    associative       map each page to an arbitrary cache line
    set-associative   map each page to a specific set of cache
                      lines that are mapped arbitrarily

Supported Replacement Algorithms:
    random       randomly choose a cache line to replace
    lfu          replace the cache line that has been used the least since it was brought in
    lru          replace the cache line that has been used the longest time ago since it was brought in
    fifo         replace the next cache line in a first-in first-out queue

Supported Access Patterns:
    random             randomly choose addresses
    full-sequential    reads the entire RAM sequentially
    random-sequential  reads from a random address to a random address
    random-pages       chooses a random page to read in its entirety
    probability        choose a random address, and have a random chance
                       of moving to a different page
    log-file