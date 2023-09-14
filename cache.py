from dataclasses import dataclass


class Cache:

    def __init__(self, block_size, cache_size, memory_size, k):
        self.num_of_lines = cache_size // block_size
        self.lines = [CacheLines] * self.num_of_lines
        self.k = k
        self.replace_count = 0


    def read(tag: int) -> int:
        pass


    def map(address: int) -> int:
        pass


    def replace(start_index: int, end_index: int, tag: int) -> None:
        pass








@dataclass
class CacheLines:

    valid : bool = False
    tag : int
    access_count : int = 0
