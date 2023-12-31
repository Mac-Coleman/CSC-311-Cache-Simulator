#Author: Torii Greiskalns
import math
import random
import sys

class AddressGenerator:
    """
    Class created and maintained by Torii
    """
    def __init__(self,ms:int,page_size:int,pattern:int):
        self.probability = .35
        self.pattern = pattern
        self.max_size = ms
        self.pointer = 0
        self.limit = 0
        self.page_size = page_size
        self.patternDict = {
            0: self.random,
            1: self.read_full_page,
            2: self.random_sequential,
            3: self.full_ram_sequential,
            4: self.probability_based_locality,
        }

    def generate_address(self):
        return self.patternDict.get(self.pattern)()
    
    def get_random_page(self):
        return random.randint(0, self.max_size//self.page_size-1)*self.page_size
    
    def set_probability(self, prob: float):
        self.probability = prob

    #different algorithms for generating input patterns 
    def random(self):# random adress through the entire RAM
        return random.randint(0, self.max_size-1)
    
    def read_full_page(self):#reads an entire page, then finds anoher random page
        if(self.pointer == self.limit):
            self.pointer = self.get_random_page()
            self.limit = self.pointer + self.page_size-1
        else:
            self.pointer += 1
        return self.pointer
    
    def random_sequential(self):#Reads a random section of RAM sequentially, then finds a new section
        if(self.pointer == self.limit):
            self.pointer = random.randint(0, self.max_size-1)
            self.limit=random.randint(self.pointer, self.max_size-1)
        else:
            self.pointer += 1

        return self.pointer
    
    def full_ram_sequential(self):#reads the entire RAM sequentially
        if(self.pointer == self.limit):
            self.pointer = 0
            self.limit = self.max_size-1
        else:
            self.pointer += 1

        return self.pointer
    
    def probability_based_locality(self):# start at a random point on a random page, and there is a (probability)% chance that 
                                        #you remain on that page for the next read
        if(self.pointer==self.limit):
            self.pointer=self.get_random_page()
            self.limit=-1# this is the case for the first call only, to stop the first page usually being 0
        else:
            if(random.random()>self.probability):
                self.pointer=self.get_random_page()
        return random.randint(self.pointer,self.pointer+self.page_size-1)

class AddressTraceGenerator(AddressGenerator):# a seperate generator class to allow reading from a trace file
    def __init__(self, file_name: str, memory_size: int, wrap_addresses: bool, max_length: int):

        self.file_name=file_name
        self.memory_size=memory_size
        self.wrap_addresses=wrap_addresses
        self.max_length=max_length
        self.file=None
        self.open_file()

        self.address_bitmask = 2**math.ceil(math.log(memory_size, 2)) - 1
        """
        Opens file 'file_name' and read it line by line.
        Get the address from each line, ignore lines starting with "--" or "=="
        Split each line by " ", take second element and split by ","
        First element of that result is the address.

        Wrap addresses within memory_size if wrap_addresses is true, otherwise
        throw error.

        Read only max_length addresses from file.
        """
    def open_file(self):
        self.file=open(self.file_name)

    def close_file(self):
        self.file.close()

    def generate_address(self):
        while True:
            line=self.file.readline()

            if not line:
                raise StopIteration
            
            if not line.startswith(("=", "-")):
                try:
                    return int(line.split(" ")[2].split(",")[0], 16) & self.address_bitmask
                except:
                    pass
               