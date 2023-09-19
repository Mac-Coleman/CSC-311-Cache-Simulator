CSC 311 Cache Simulator Project

Authors: Brodie McCuen, Torii Greiskalns, Mac Coleman
Block 1, 2023
Cornell College

This project provides a simulator for different types of caches.

Usage:
python cache_simulator.py <CACHE-TYPE> <READS> [options]

The CACHE_TYPE and READS arguments are required positional arguments.
  CACHE_TYPE defines the type of cache being simulated
  READS defines the number of accesses made to that cache.

Optional Arguments:
  -a, --access-pattern <pattern>  the access pattern to use
                                  can be a path to a Valgrind Lackey trace file
  -b, --block-size <size>         set the cache line and memory page size
                                  default: 4KB
  -c, --cache-size <size>         size of the cache
                                  default: 32KB
  -d, --disable-output-files      disables writing of output files hit_and_miss.txt,
                                  stats.txt, and locality.txt
  -h, --help                      display a help message
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

EXAMPLES:
    python cache_simulator.py direct 1M
        simulates 1M memory accesses on a cache with default settings
    python cache_simulator.py associative 3K -m 1G -c 512K -b 2K
        simulates 3M memory accesses on 1 gigabyte of physical memory on a 512-kilobyte cache with 2-kilobyte block_size
    python cache_simulator.py set-associative -k 4 150
        simulates 150 memory accesses on a 4-way set-associative cache with default setting
    python cache_simulator.py associative 1M -r fifo
        simulates one million accesses on a associative cache using the fifo replacement_algorithm
    python cache_simulator.py direct 250K --access-pattern=random-pages
        simulate 250 thousand accesses on a direct cache with default settings using the random-pages access pattern
    python cache_simulator.py set-associative 100 -k 2 -a probability -p 0.3
        simulate 100 accesses on a 2-way set-associative cache with the probability access pattern with a 30% chance of staying on the same page
    python cache_simulator.py direct 475 -a traces/sum.log
        simulate 475 accesses on a direct cache with an access pattern defined in the memory trace file "traces/sum.log"

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
    <log-file>         a memory trace file produced with Valgrind's Lackey tool

Input Files:
    The program can accept memory access trace files as inputs if they have a .log extension.

    The files must be in the Valgrind Lackey format. Two examples are provided in traces/hello_world.log
    and traces/sum.log. Generated addresses are mapped to fit within the size of the memory in order to
    prevent invalid accesses. Only the base of each access in the trace file is used as the data size is
    small compared to the page size and unlikely to cause a page fault for the purposes of our simulation.

    To generate your own trace file, use Valgrind's Lackey tool with the following command:
        `valgrind --log-fd=1 --tool=lackey -v --trace-mem=yes {program} > {filename.log}`

        where {program} is the program you want to generate a memory trace for (such as `ls`)
        and {filename.log} is the name of your output trace file.

        Beware that trace files are extremely large for small inputs.
    
    The two provided trace files were generated from a basic hello world program and a program that
    finds the sum of an array of integers in C.

Output Files:
    The program outputs three files, hit_and_miss.txt, locality.txt, and stats.txt

    hit_and_miss.txt:
        Each line contains a address and its read result in the cache.
        Every line indicates whether an access made to a particular address
        resulted in a hit or a miss.

    locality.txt:
        Each line contains a page number and the number of times it was accessed.
        Each page number must have been accessed at least once in order to appear in this file.
        The first column indicates the page number and the second the number of times it was accessed.

    stats.txt:
        Records statistics about the simulation including the number of hits, the hit ratio, the total
        number of reads, and information relating to the type of cache system that was simulated.

Errors:
    Errors that we have determined are incompatible with continuing the program will immediately cause the program to exit.
    Errors which can be corrected or ignored will allow the program to continue.
    For example, trace files containing invalid lines will simply have their invalid lines ignored.