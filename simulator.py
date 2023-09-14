
from address_generator import AddressGenerator 
def simulator(max_size:int, page_size:int, cache_size:int, map_algorithm, set_size:int, reads:int):
    hit_record=list[bool]
    #cache=cache()
    address_maker=AddressGenerator(max_size)
    for i in reads:
        address=address_maker.generate_address(max_size)
        #hit_record.append(cache.read(address))
    #replacements=cache.getReplacementCount()