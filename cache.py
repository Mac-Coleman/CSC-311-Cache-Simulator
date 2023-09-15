from dataclasses import dataclass

class Cache:

    def __init__(self, block_size, cache_size, memory_size, k):

        if not is_power_of_two(block_size):
            raise ValueError("Block size must be a power of two!")
        
        if not is_power_of_two(cache_size):
            raise ValueError("Cache size must be a power of two!")
        
        if not is_power_of_two(k):
            raise ValueError("Set size must be a power of two!")
        
        if memory_size < cache_size:
            raise ValueError("Memory size must be greater than cache size!")
        
        if cache_size < block_size:
            raise ValueError("Cache size must be greater than block size!")

        self.num_of_lines = cache_size // block_size
        self.block_size = block_size

        self.lines = [CacheLine() for x in range(self.num_of_lines)]
        # List comprehension in order to avoid shallow copy

        self.k = k
        self.replace_count = 0


    def read(self, address: int) -> int:
        page_number = address // self.block_size
        upper, lower = self.direct_map(page_number)

        tag = page_number // (self.num_of_lines // self.k)
        hit = self.check_hit(lower, upper, tag)

        if not hit:
            self.replace(lower, upper, tag)
        
        return hit

    def direct_map(self, page_number: int) -> tuple[int, int]:
        set_index = (page_number) % (self.num_of_lines // self.k) # Get set number

        lower_index = set_index * self.k
        upper_index = set_index * self.k + self.k
        # Only a direct mapping for now!
        return upper_index, lower_index
    
    def check_hit(self, start_index: int, end_index: int, tag: int) -> bool:
        
        # Traverse lines in set, check if they are hits.
        for i in range(start_index, end_index):
            if self.lines[i].valid and self.lines[i].tag == tag:
                self.lines[i].access_count += 1
                return True

        return False


    def replace(self, start_index: int, end_index: int, tag: int) -> None:
        if start_index + 1 == end_index: # We have only one choice!
            self.lines[start_index].tag = tag
            self.lines[start_index].valid = True
            print(f"\treplacing {start_index}")

        self.replace_count += 1


@dataclass
class CacheLine:

    valid : bool = False
    tag : int = 0
    access_count : int = 0

def is_power_of_two(num: int) -> bool:
    # For any power of two, its binary interpretation can have exactly one set bit.
    return num.bit_count() == 1