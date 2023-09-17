from dataclasses import dataclass
from operator import attrgetter
import math
import random

class Cache:

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
    
    def read(self, address: int) -> tuple[int, bool]:
        pass
    
    def get_replacement_count(self) -> int:
        return self.replace_count

class DirectCache(Cache):
    def __init__(self, block_size: int, cache_size: int, memory_size: int):
        super(DirectCache, self).__init__(block_size, cache_size, memory_size)
        self.lines = [CacheLine() for _ in range(self.num_of_lines)]
    
    def read(self, address: int) -> tuple[int, bool]:
        page = address % self.block_size
        line = page % self.num_of_lines
        tag = page // self.num_of_lines

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
        self.lines = CacheSet(self.num_of_lines, "lru")
    
    def read(self, address: int) -> tuple[int, bool]:
        page_number = address // self.block_size
        hit = self.lines.read(page_number)
        if not hit:
            self.replace_count += 1
        return page_number, hit

class SetAssociativeCache(Cache):
    def __init__(self, block_size: int, cache_size: int, memory_size: int, replacement_algorithm: str, set_size: int):

        if not is_power_of_two(set_size):
            raise ValueError("Set size 'k' must be a power of two!")
        
        super(SetAssociativeCache, self).__init__(block_size, cache_size, memory_size)
        self.num_of_sets = self.num_of_lines // set_size
        self.sets = [CacheSet(set_size, replacement_algorithm) for x in range(self.num_of_sets)]
    
    def read(self, address: int) -> tuple[int, bool]:
        page = address // self.block_size
        set_index = page % self.num_of_sets
        tag = page // self.num_of_sets

        s = self.sets[set_index]
        hit = s.read(tag)

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
        self.lines = [CacheLine() for x in range(lines)]
        self.fifo_pointer = 0
        algo_dict = {
            "lru": self.replace_lru,
            "fifo": self.replace_fifo,
            "random": self.replace_fifo
        }
        self.replacement_algorithm = algo_dict[replacement_algorithm]
    
    def read(self, tag: int) -> bool:
        """
        Returns Bool, whether line was replaced or not
        """
        cl = self.lines[self.lines.index(tag)] if tag in self.lines else None
        flag = True

        if cl == None:
            flag = False
            cl = self.replacement_algorithm(tag)
        
        cl.access_count += 1
        return flag
    
    def replace_lru(self, tag: int) -> CacheLine:
        l = min(self.lines, key=attrgetter("access_count"))
        l.tag = tag
        l.valid = True
        return l

    def replace_lfu(self, tag: int) -> CacheLine:
        l = min(self.lines, key=attrgetter("access_count"))
        l.tag = tag
        l.valid = True
        l.access_count = 0  # been accessed one time
        return l

    def replace_fifo(self, tag: int) -> CacheLine:
        l = self.lines[self.fifo_pointer]
        l.tag = tag
        l.valid = True
        self.fifo_pointer += 1
        if self.fifo_pointer == len(self.lines):
            self.fifo_pointer = 0

        return l
        

    def replace_random(self, tag: int) -> CacheLine:
        l = random.choice(self.lines)
        l.tag = tag
        l.valid = True
        return l
