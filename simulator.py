
from address_generator import address_generator 
def simulator(max_size:int, page_size:int, cache_size:int, map_algorithm, set_size:int, reads:int):
    hit_record=list[bool]
    #cache=cache()
    address_generator=adress_generator()
    for i in 10:
        address=generate_address(max_size)
        #hit_record.append(cache.read(address))
    #replacements=cache.getReplacementCount()