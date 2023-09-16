
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

    ### Writes a new line to the file
    def add(self, index, result):
        if result:
            self.output_file.write("{0:x} {1}\n".format(index, "hit"))
        else:
            self.output_file.write("{0:x} {1}\n".format(index, "miss"))