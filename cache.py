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
            raise ValueError("Block size must be a power of two!")
        
        if not is_power_of_two(cache_size):
            raise ValueError("Cache size must be a power of two!")
        
        if not is_power_of_two(memory_size):
            raise ValueError("Memory size must be a power of two!")
        
        self.block_size = block_size
        self.cache_size = cache_size
        self.memory_size = memory_size
        self.replace_count = 0

        self.num_of_lines = self.cache_size // self.block_size
    
    def read(self, address: int, time: int) -> tuple[int, bool]:
        pass
    
    def get_replacement_count(self) -> int:
        return self.replace_count

class DirectCache(Cache):
    def __init__(self, block_size: int, cache_size: int, memory_size: int):
        super(DirectCache, self).__init__(block_size, cache_size, memory_size)
        self.lines = [CacheLine() for _ in range(self.num_of_lines)]
    
    def read(self, address: int) -> tuple[int, bool]:
        # removes word offset
        page = address // self.block_size
        # makes the line number (right hand side of bits)
        line = page % self.num_of_lines
        # makes the tag (left hand side of bits)
        tag = page // self.num_of_lines

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
        page_number = address // self.block_size
        # call read method in cacheset
        hit = self.lines.read(page_number, time)
        if not hit:
            self.replace_count += 1

        return page_number, hit

class SetAssociativeCache(Cache):
    def __init__(self, block_size: int, cache_size: int, memory_size: int, replacement_algorithm: str, set_size: int):

        super(SetAssociativeCache, self).__init__(block_size, cache_size, memory_size)

        if not is_power_of_two(set_size):
            raise ValueError("Set size 'k' must be a power of two!")
        
        if set_size > self.num_of_lines:
            raise ValueError(f"Set size must be less than or equal to the number of lines in the cache! Lines: {self.num_of_lines}")
        

        self.num_of_sets = self.num_of_lines // set_size
        self.sets = [CacheSet(set_size, replacement_algorithm) for x in range(self.num_of_sets)]
    
    def read(self, address: int, time: int) -> tuple[int, bool]:
        # removes word offset
        page = address // self.block_size
        # takes the set (right hand side of page)
        set_index = page % self.num_of_sets
        # takes the tag (left hand side of page)
        tag = page // self.num_of_sets

        s = self.sets[set_index]
        hit = s.read(tag, time)

        if not hit:
            self.replace_count += 1
        return page, hit

def is_power_of_two(num: int) -> bool:
    # For any power of two, its binary interpretation can have exactly one set bit.
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
    
    def read(self, tag: int, time: int) -> bool:
        """
        Returns Bool, whether line was replaced or not
        """
        cl = self.lines[self.lines.index(tag)] if tag in self.lines else None
        flag = True

        if cl == None:
            flag = False
            if self.is_full:
                cl = self.replacement_algorithm(tag)
            else:
                cl = self.lines[self.next_available]
                cl.valid = True
                next_available += 1
                self.is_full = next_available == self.lines
            
        # updates chosen line information
        cl.access_count += 1
        cl.access_time = time
        return flag
   

    def replace_lru(self, tag: int) -> CacheLine:
        l = min(self.lines, key=attrgetter("access_time"))
        l.tag = tag
        return l

    def replace_lfu(self, tag: int) -> CacheLine:
        l = min(self.lines, key=attrgetter("access_count"))
        l.tag = tag
        l.access_count = 0  # been accessed one time
        return l

    def replace_fifo(self, tag: int) -> CacheLine:
        l = self.lines[self.fifo_pointer]
        l.tag = tag
        self.fifo_pointer += 1
        if self.fifo_pointer == len(self.lines):
            self.fifo_pointer = 0

        return l
        
    def replace_random(self, tag: int) -> CacheLine:
        l = random.choice(self.lines)
        l.tag = tag
        l.valid = True
        return l
