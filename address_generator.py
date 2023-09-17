import random

class AddressGenerator:
    def __init__(self,ms:int,pattern:int,page_size:int):
        self.pattern=pattern
        self.max_size=ms
        self.pointer=0
        self.limit=0
        self.page_size=page_size
        self.patternDict={
            0:self.random_pattern,
            1:self.read_full_page,
        }
    def generate_address(self):
        return self.patternDict.get(self.pattern)()
    def get_random_page(self):
        return random.randint(0,self.max_size/self.page_size)
    #different algorithms for generating input patterns 
    def random_pattern(self):
        return random.randint(0,self.max_size)
    def read_full_page(self):
        if(self.pointer==self.limit):
            self.pointer=self.get_random_page()
            self.limit=self.pointer+self.page_size
        else:
            pointer+=1
        return pointer