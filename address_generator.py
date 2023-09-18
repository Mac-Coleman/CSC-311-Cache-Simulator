#Author: Torii Greiskalns
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
    
    def set_probability(self,prob: int):
        self.probability = prob

    #different algorithms for generating input patterns 
    def random(self):
        return random.randint(0, self.max_size-1)
    
    def read_full_page(self):
        if(self.pointer == self.limit):
            self.pointer = self.get_random_page()
            self.limit = self.pointer + self.page_size-1
        else:
            self.pointer += 1
        return self.pointer
    
    def random_sequential(self):
        if(self.pointer == self.limit):
            self.pointer = random.randint(0, self.max_size-1)
            self.limit=random.randint(self.pointer, self.max_size-1)
        else:
            self.pointer += 1

        return self.pointer
    
    def full_ram_sequential(self):
        if(self.pointer == self.limit):
            self.pointer = 0
            self.limit = self.max_size-1
        else:
            self.pointer += 1

        return self.pointer
    
    def probability_based_locality(self):
        if(self.pointer==self.limit):
            self.pointer=self.get_random_page()
            self.limit=-1# this is the case for the first call only, to stop the first page usually being 0
        else:
            if(random.random()>self.probability):
                self.pointer=self.get_random_page()
        return random.randint(self.pointer,self.pointer+self.page_size-1)

class AddressTraceGenerator:
    def __init__(self, file_name: str, memory_size: int, wrap_addresses: bool, max_length: int):
        self.pointer=0
        self.file_name=file_name
        self.memory_size=memory_size
        self.wrap_addresses=wrap_addresses
        self.max_length=max_length
        self.file=None
        self.open_file()
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
        found=False
        line1=None
        while found is not True:
            line=self.file.readline()
            if(line[0] != "=" and line[0] != "-"):
                try:
                    line1=line.split(" ")[2].split(",")[0]
                    found=True
                except:
                    print("bad input, ignoring "+line)
                    # doesnt exit, trys to keep going and ignore the bad input
        if(line1 is not None):
            intLine=int(line1,16)
            if(intLine>self.memory_size):
                if(self.wrap_addresses):
                    return intLine%self.memory_size
                else:
                    print("Invalid Memory Line: "+str(intLine))
                    sys.exit(1)
            else:
                return intLine
        else:
            print("Line not found")
            sys.exit(1)
                
            

if __name__=="__main__":
    ag=AddressTraceGenerator("./traces/hello_world.log",8096,False,600)
    print(ag.generate_address())
    print(ag.generate_address())    
    print(ag.generate_address())