from dataclasses import dataclass
import math

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
    
    def read(self, address: int) -> tuple[int, bool]:
        pass
    
    def get_replacement_count(self) -> int:
        return self.replace_count

class DirectCache(Cache):
    def __init__(self, block_size: int, cache_size: int, memory_size: int):
        super(DirectCache, self).__init__(block_size, cache_size, memory_size)
        self.num_of_lines = self.cache_size // self.block_size
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
    pass

class SetAssociativeCache(Cache):
    pass

@dataclass
class CacheLine:

    valid : bool = False
    tag : int = 0
    access_count : int = 0

    def __eq__(self, other) -> bool:
        return self.tag == other and self.valid

def is_power_of_two(num: int) -> bool:
    # For any power of two, its binary interpretation can have exactly one set bit.
    return num.bit_count() == 1