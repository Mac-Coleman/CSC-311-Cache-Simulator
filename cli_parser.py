from enum import Enum

class OptionFormat(Enum):
    COMBINED_SHORT = 0
    COMBINED_LONG = 1
    SEPARATE_SHORT = 2
    SEPARATE_LONG = 3

def parse_arguments(args: list[str]):
    file_name = args[0]

    # Positional:
    #   Cache Type
    #     If set-associative: k
    #   Reads
    # Optional:
    #   Memory size
    #   Block size
    #   Cache size

    consumed = [False for element in range(len(args))]
    # Makes a list of bools to mark options as consumed.

    print("Memory size:", get_option_value(args, consumed, "--memory-size", "-m"))
    print("Block size:", get_option_value(args, consumed, "--block-size", "-b"))
    print("Cache size:", get_option_value(args, consumed, "--cache-size", "-c"))
    print("Reads:", get_option_value(args, consumed, "--reads", "-r"))

def get_flag_presence(args: list[str], consumed: list[bool], long: str, short: str) -> bool:
    
    long_index = args.index(long)
    short_index = args.index(short)

    if long_index >= 0:
        consumed[long_index] = True
    
    if short_index >= 0:
        consumed[short_index] = True
    
    return long_index >= 0 or short_index >= 0

def get_option_value(args: list[str], consumed: list[bool], long: str, short: str) -> None | str:
    """
    Retrieves the value for an option from a list. Returns None if not present.
    long: The long-form name of the option. (e.g. "--block-size")
    short: the short-form name of the option. (e.g. "-b")
    Consumes elements from args by removing them when they are found.
    """

    option_style = get_option_index(args, long, short)

    if not option_style:
        return None # The option is not present.
    
    if option_style[0] == OptionFormat.COMBINED_SHORT:
        # The arguments are in the same element of the args list.

        consumed[option_style[1]] = True
        return args[option_style[1]][len(short):]
    
    if option_style[0] == OptionFormat.COMBINED_LONG:
        # The arguments are in the same element of the args list.
        index = args[option_style[1]].index("=") + 1

        consumed[option_style[1]] = True
        return args[option_style[1]][index:]
    
    index = option_style[1]+1
    if index >= len(args):
        raise ValueError(f"Option {option_style[1]} was given but no value was specified.")
    
    args[index]
    consumed[option_style[1]] = True
    consumed[index] = True
    return args[index]

def get_option_index(args: list[str], long: str, short: str) -> tuple[OptionFormat, int] | None:
    for (index, argument) in enumerate(args):
        if argument.startswith(long):
            type = OptionFormat.COMBINED_LONG if "=" in argument else OptionFormat.SEPARATE_LONG
            return (type, index)
        
        if argument.startswith(short):
            type = OptionFormat.SEPARATE_SHORT if len(argument) == len(short) else OptionFormat.COMBINED_SHORT
            return (type, index)
    
    return None
