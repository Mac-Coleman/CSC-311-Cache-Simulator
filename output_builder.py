
class OutputBuilder:

    def __init__(self, replacement_count, hit_count, miss_count, read_locality):
        self.replacement_count = replacement_count
        self.hit_count = hit_count
        self.miss_count = miss_count
        self. read_locality = read_locality
        self.output_file

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

    ### Writes a new line to the file
    def add(self, index, result):
        if result:
            self.output_file.write("{0:2d} {1:3d}".format(index, "hit"))
        elif result:
            self.output_file.write("{0:2d} {1:3d}".format(index, "miss"))
        else:
            print("Something is Wrong!")