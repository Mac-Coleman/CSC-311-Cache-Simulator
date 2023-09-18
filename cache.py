"""
Set-associative Cache class originally written by Brodie and Mac

Refactored into inheritance-based classes by Mac
Brodie wrote replacement algorithms
Changes to bitwise operations by Mac
"""

from dataclasses import dataclass
from operator import attrgetter
import math
import random

class Cache:
    '''
    Parent class for DirectCache, AssociativeCache, and SetAssociativeCache
    Initialized with block size, cache size, and main memory size, must be in powers of two
    Each Cache Class has seperate logic for calculating cache hits and cache misses.
    '''
    def __init__(self, block_size: int, cache_size: int, memory_size: int):

        if not is_power_of_two(block_size):
            raise ValueError(f"Invalid block size: {block_size}. Block size must be a power of two!")
        
        if not is_power_of_two(cache_size):
            raise ValueError(f"Invalid cache size: {cache_size}. Cache size must be a power of two!")
        
        if not is_power_of_two(memory_size):
            raise ValueError(f"Invalid memory size: {memory_size}. Memory size must be a power of two!")
    
        if block_size > cache_size:
            raise ValueError(f"Invalid block size. Block size must be less than or equal to cache size.")

        if cache_size > memory_size:
            raise ValueError(f"Invalid cache size: Cache size must be less than or equal to memory size.")
        
        self.block_size = block_size
        self.cache_size = cache_size
        self.memory_size = memory_size
        self.replace_count = 0

        self.num_of_lines = self.cache_size // self.block_size

        self.offset_length = int(math.log(block_size, 2))
    
    def read(self, address: int, time: int) -> tuple[int, bool]:
        pass
    
    def get_replacement_count(self) -> int:
        return self.replace_count

class DirectCache(Cache):
    def __init__(self, block_size: int, cache_size: int, memory_size: int):
        super(DirectCache, self).__init__(block_size, cache_size, memory_size)
        self.lines = [CacheLine() for _ in range(self.num_of_lines)]
        self.line_number_length = int(math.log(self.num_of_lines, 2))
        self.line_number_bitmask = 2**self.line_number_length - 1
    
    def read(self, address: int, time: int) -> tuple[int, bool]:
        # removes word offset
        page = address >> self.offset_length
        # makes the line number (right hand side of bits)
        line = page & self.line_number_bitmask
        # makes the tag (left hand side of bits)
        tag = page >> self.line_number_length

        # chosen line
        cl = self.lines[line]
        hit = cl == tag

        if not hit:
            cl.tag = tag
            cl.valid = True
            self.replace_count += 1
        cl.access_count += 1

        return page, hit


class AssociativeCache(Cache):
    def __init__(self, block_size: int, cache_size: int, memory_size: int, replacement_algorithm: str):
        super(AssociativeCache, self).__init__(block_size, cache_size, memory_size)
        # makes a set of cachelines
        self.lines = CacheSet(self.num_of_lines, replacement_algorithm)
    
    def read(self, address: int, time: int) -> tuple[int, bool]:
        # removes word offset
        page_number = address >> self.offset_length
        # call read method in cacheset
        hit, replacement = self.lines.read(page_number, time)
        if not hit and replacement:
            self.replace_count += 1

        return page_number, hit

class SetAssociativeCache(Cache):
    def __init__(self, block_size: int, cache_size: int, memory_size: int, replacement_algorithm: str, set_size: int):

        super(SetAssociativeCache, self).__init__(block_size, cache_size, memory_size)

        if not is_power_of_two(set_size):
            raise ValueError(f"Invalid set size: {set_size}. Set size 'k' must be a power of two!")
        
        if set_size > self.num_of_lines:
            raise ValueError(f"Invalid set size: {set_size}. Set size must be less than or equal to the number of lines in the cache! Lines: {self.num_of_lines}")
        
        if set_size <= 0:
            raise ValueError(f"Invalid set size: {set_size}. Set size must be a positive, nonzero integer.")
        

        self.num_of_sets = self.num_of_lines // set_size
        self.sets = [CacheSet(set_size, replacement_algorithm) for x in range(self.num_of_sets)]

        self.set_number_length = int(math.log(self.num_of_sets, 2))
        self.set_number_bitmask = 2**self.set_number_length - 1
    
    def read(self, address: int, time: int) -> tuple[int, bool]:
        # removes word offset
        page = address >> self.offset_length
        # takes the set (right hand side of page)
        set_index = page & self.set_number_bitmask
        # takes the tag (left hand side of page)
        tag = page >> self.set_number_length

        s = self.sets[set_index]
        hit, replacement = s.read(tag, time)

        # replacement happens
        if not hit and replacement:
            self.replace_count += 1

        return page, hit

def is_power_of_two(num: int) -> bool:
    # For any power of two, its binary interpretation can have exactly one set bit.
    # Written by Mac
    return num.bit_count() == 1

@dataclass
class CacheLine:

    valid : bool = False
    tag : int = 0
    access_count : int = 0
    access_time : int = 0

    def __eq__(self, other) -> bool:
        return self.tag == other and self.valid


class CacheSet:
    def __init__(self, lines, replacement_algorithm):
        self.length = lines
        self.lines = [CacheLine() for x in range(lines)]
        self.fifo_pointer = 0
        self.next_available = 0
        self.is_full = False
        algo_dict = {
            "lru": self.replace_lru,
            "lfu" : self.replace_lfu,
            "fifo": self.replace_fifo,
            "random": self.replace_fifo
        }
        self.replacement_algorithm = algo_dict[replacement_algorithm]
    
    def read(self, tag: int, time: int) -> tuple[bool, bool]:
        """
        Returns Bool, whether line was replaced or not
        """
        # Section for Cache Hit
        hit = tag in self.lines
        if hit:
            chosen_line = self.lines[self.lines.index(tag)]
            return hit, False
        
        # Section for Cache miss / Replacement
        if self.is_full:
            chosen_line = self.replacement_algorithm(tag)
            return hit, True
        else:
            chosen_line = self.lines[self.next_available]
            chosen_line.valid = True
            self.next_available += 1
            self.is_full = self.next_available == self.length
            return hit, False
   

    def replace_lru(self, tag: int) -> CacheLine:
        line = min(self.lines, key=attrgetter("access_time"))
        line.tag = tag
        return line

    def replace_lfu(self, tag: int) -> CacheLine:
        line = min(self.lines, key=attrgetter("access_count"))
        line.tag = tag
        line.access_count = 0  # been accessed one time
        return line

    def replace_fifo(self, tag: int) -> CacheLine:
        line = self.lines[self.fifo_pointer]
        line.tag = tag
        self.fifo_pointer += 1
        if self.fifo_pointer == len(self.lines):
            self.fifo_pointer = 0

        return line
        
    def replace_random(self, tag: int) -> CacheLine:
        line = random.choice(self.lines)
        line.tag = tag
        return line
