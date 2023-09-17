import random

class AddressGenerator:
    def __init__(self,ms:int,page_size:int,pattern:int):
        self.pattern=pattern
        self.max_size=ms
        self.pointer=0
        self.limit=0
        self.page_size=page_size
        self.patternDict={
            0:self.random,
            1:self.read_full_page,
            2:self.random_sequential,
            3:self.full_ram_sequential
        }
    def generate_address(self):
        return self.patternDict.get(self.pattern)()
    def get_random_page(self):
        return random.randint(0,self.max_size//self.page_size-1)*self.page_size
    #different algorithms for generating input patterns 
    def random(self):
        return random.randint(0,self.max_size)
    def read_full_page(self):
        if(self.pointer==self.limit):
            self.pointer=self.get_random_page()
            self.limit=self.pointer+self.page_size-1
        else:
            self.pointer+=1
        return self.pointer
    def random_sequential(self):
        if(self.pointer==self.limit):
            self.pointer=random.randint(0,self.max_size-1)
            self.limit=random.randint(self.pointer,self.max_size-1)
        else:
            self.pointer+=1
        return self.pointer
    def full_ram_sequential(self):
        if(self.pointer==self.limit):
            self.pointer=0
            self.limit=self.max_size-1
        else:
            self.pointer+=1
        return self.pointer



if __name__=="__main__":
    ag=AddressGenerator(256,16,3)
    for i in range(128):
        print(ag.generate_address())