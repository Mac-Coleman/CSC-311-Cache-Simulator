
from address_generator import AddressGenerator 
from output_builder import OutputBuilder
from cache import Cache
def simulator(max_size:int, page_size:int, cache_size:int, map_algorithm, set_size:int, reads:int):
    cache=Cache(page_size, cache_size,max_size,set_size)
    output_builder=OutputBuilder()
    output_builder.open_output()
    hit_counter=0
    total_counter=0
    address_maker=AddressGenerator(max_size)
    for i in reads:
        address=address_maker.generate_address(max_size)
        locality=None#make locality based off addresses- dict{page#: access count}
        hit=cache.read(address)
        output_builder.add(i,hit)
        if(hit):
            hit_counter+=1
        total_counter+=1
    hit_ratio=hit_counter/total_counter
    #replacements=cache.getReplacementCount()
    output_builder.close()
    output_builder.print_data(hit_ratio,replacements,locality)
