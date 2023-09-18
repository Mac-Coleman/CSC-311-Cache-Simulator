
class OutputBuilder:

    def __init__(self):
        self.open_output()

    ### Prints Output data to the consol
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
        with open("locality.txt", "w", encoding='utf-8') as f:
            pages = sorted(locality.keys())
            for page in pages:
                f.write("{0:{width}x}: {1}\n".format(page, locality[page], width=page_length))

    def write_stats_file(self, hits: int, total: int, replacements: int):
        with open("stats.txt", "w") as f:
            f.write(f"Hit ratio: {hits/total * 100:06f}%\n")
            f.write(f"Hits: {hits}\n")
            f.write(f"Misses: {total - hits}\n")
            f.write(f"Accesses: {total}\n")
            f.write(f"Replacements: {replacements}\n")
    
    ### Writes a new line to the file
    def add(self, index, result):
        if result:
            self.output_file.write("{0:x} {1}\n".format(index, "hit"))
        else:
            self.output_file.write("{0:x} {1}\n".format(index, "miss"))