import random

class AddressGenerator:
    def __init__(self,ms:int):
        self.max_size=ms
    def generate_address(self):
        return random.randint(0,self.max_size)