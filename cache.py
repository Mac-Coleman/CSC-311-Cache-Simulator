from dataclasses import dataclass
import math

class Cache:

    def __init__(self, block_size, cache_size, memory_size, k, algorithm):

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

        self.offset_length = math.ceil(math.log(block_size, 2))
        self.page_number_length = math.ceil(math.log(memory_size, 2)) - self.offset_length
        self.set_number_length = math.ceil(math.log(self.num_of_lines // k, 2))
        self.tag_length = self.page_number_length - self.set_number_length

        self.set_number_bitmask = 2**self.set_number_length - 1
        print("offset:",self.offset_length)
        print("page num length:", self.page_number_length)
        print("lines:", self.num_of_lines)
        print("set number length:", self.set_number_length)
        print("tag length:", self.tag_length)

        algo_dict = {
            "lru": self.replace_lru
        }

        try:
            self.replacement_algorithm = algo_dict[algorithm]
        except KeyError:
            raise ValueError(f"Invalid replacement algorithm: {algorithm}")

        self.lines = [CacheLine() for x in range(self.num_of_lines)]
        # List comprehension in order to avoid shallow copy

        self.k = k
        self.replace_count = 0


    def read(self, address: int) -> int:
        page_number = address >> self.offset_length
        upper, lower = self.direct_map(page_number)

        tag = page_number >> self.set_number_length
        hit = self.check_hit(lower, upper, tag)

        #print(f"{page_number:08x}, {tag:08x}")

        if not hit:
            self.replacement_algorithm(lower, upper, tag)
        
        return hit

    def direct_map(self, page_number: int) -> tuple[int, int]:
        set_index = page_number & self.set_number_bitmask # Get set number

        lower_index = set_index * self.k
        upper_index = lower_index + self.k
        # Only a direct mapping for now!
        return upper_index, lower_index
    
    def check_hit(self, start_index: int, end_index: int, tag: int) -> bool:
        
        # Traverse lines in set, check if they are hits.
        i = self.lines.index(tag, start_index, end_index) if tag in self.lines[start_index:end_index] else False

        if i is not False and self.lines[i].valid:
            return True

        return False


    def replace(self, start_index: int, end_index: int, tag: int) -> None:
        if start_index + 1 == end_index: # We have only one choice!
            self.lines[start_index].tag = tag
            self.lines[start_index].valid = True
            #print(f"\treplacing {start_index}")
        
        self.replace_lru(start_index, end_index, tag)

        self.replace_count += 1
    
    def replace_lru(self, start_index: int, end_index: int, tag: int) -> None:
        min_used = self.lines[start_index].access_count
        min_index = start_index

        for i in range(start_index, end_index):
            if min_used > (ac := self.lines[i].access_count):
                min_index = i
                min_used = ac
        
        c = self.lines[min_index]
        c.tag = tag
        c.access_count += 1
        c.valid = True
    
    def get_replacement_count(self) -> int:
        return self.replace_count


@dataclass
class CacheLine:

    valid : bool = False
    tag : int = 0
    access_count : int = 0

    def __eq__(self, other) -> bool:
        return self.tag == other

def is_power_of_two(num: int) -> bool:
    # For any power of two, its binary interpretation can have exactly one set bit.
    return num.bit_count() == 1