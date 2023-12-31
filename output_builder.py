from cli_parser import OptionDict

class OutputBuilder:

    def __init__(self):
        """
        Class originally written by Brodie
        """
        self.open_output()

    ### Prints Output data to the console
    def print_data(self, hit_ratio, replacement_count, locality):
        print(f"Hit Ratio: {hit_ratio}\nReplacement Count: {replacement_count}")
        # will print actually locality information later
        print("locality")

    ### Opens a File
    def open_output(self):
        self.output_file = open('hit_and_miss.txt', 'w', encoding='utf-8')

    ### Closes a file
    def close_output(self):
        self.output_file.close()
    
    def write_locality_file(self, locality: dict[int, int], page_length: int):
        """
        Writes each page number and its accesses to the file `Locality.txt`
        Written by Mac
        """
        with open("locality.txt", "w", encoding='utf-8') as f:
            pages = sorted(locality.keys())
            for page in pages:
                f.write("{0:0{width}x}: {1}\n".format(page, locality[page], width=page_length))


    def write_stats_file(self, hits: int, total: int, replacements: int, options: OptionDict):
        """
        Outputs runtime statistics to the file `stats.txt`
        Written by Mac
        """
        with open("stats.txt", "w") as f:
            f.write(f"Hit ratio: {hits/total * 100:06f}%\n")
            f.write(f"Hits: {hits}\n")
            f.write(f"Misses: {total - hits}\n")
            f.write(f"Accesses: {total}\n")
            f.write(f"Replacements: {replacements}\n")
            f.write(f"Cache Type: {options['cache_type']}\n")
            if options['cache_type'] == "set-associative":
                f.write(f"Set size: {options['k']}\n")
            f.write(f"Memory Size: {options['memory_size']}\n")
            f.write(f"Page Size: {options['block_size']}\n")
            f.write(f"Cache Size: {options['cache_size']}\n")
            f.write(f"Access Pattern: {options['access_pattern']}\n")
    
    ### Writes a new line to the file
    def add(self, address: int, result: bool):
        """
        Written by Brodie
        """
        if result:
            self.output_file.write("{0:x} {1}\n".format(address, "hit"))
        else:
            self.output_file.write("{0:x} {1}\n".format(address, "miss"))