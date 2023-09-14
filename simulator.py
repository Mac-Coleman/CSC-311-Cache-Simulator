
from address_generator import AddressGenerator 
def simulator(max_size:int, page_size:int, cache_size:int, map_algorithm, set_size:int, reads:int):
    #cache=cache()
    #output_builder=OutputBuilder()
    hit_counter=0
    total_counter=0
    address_maker=AddressGenerator(max_size)
    for i in reads:
        address=address_maker.generate_address(max_size)
        hit=None#cache.read(address)
        #outputbuilder.append(hit)
        if(hit):
            hit_counter+=1
        total_counter+=1
    hit_ratio=hit_counter/total_counter
    #replacements=cache.getReplacementCount()
    #output_builder.close()
    #output_builder.print_data(hit_ratio,locality,replacements)
    #output builder make output from replacements and hit record 