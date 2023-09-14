from enum import Enum
import sys
from typing import Callable

class OptionFormat(Enum):
    COMBINED_SHORT = 0
    COMBINED_LONG = 1
    SEPARATE_SHORT = 2
    SEPARATE_LONG = 3

def parse_arguments(args: list[str], help_handler: Callable, version_handler: Callable, run_handler: Callable):

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
    file_name = args[0]
    consumed[0] = True

    memory_size = "256MB"
    block_size = "4KB"
    cache_size = "32KB"

    run_help = get_flag_presence(args, consumed, "--help", "-h")
    run_version = get_flag_presence(args, consumed, "--version", "-v")

    if run_help:
        help_handler(file_name)
        return
    
    if run_version:
        version_handler(file_name)
        return


    memory_size_parsed = get_option_value(args, consumed, "--memory-size", "-m")
    block_size_parsed = get_option_value(args, consumed, "--block-size", "-b")
    cache_size_parsed = get_option_value(args, consumed, "--cache-size", "-c")

    if memory_size_parsed:
        memory_size = memory_size_parsed
    
    if block_size_parsed:
        block_size = block_size_parsed
    
    if cache_size_parsed:
        cache_size = cache_size_parsed

    check_unconsumed(args, consumed)

    options: dict[str, int] = {
        "memory_size": str_to_size(memory_size),
        "block_size": str_to_size(block_size),
        "cache_size": str_to_size(cache_size),
    }
    run_handler(options)

def get_flag_presence(args: list[str], consumed: list[bool], long: str, short: str) -> bool:
    

    if long in args and (long_index := args.index(long)):
        consumed[long_index] = True
        return True
    
    if short in args and (short_index := args.index(short)):
        consumed[short_index] = True
        return True
    
    return False

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
    
    if consumed[option_style[1]]:
        return None # This is already consumed. (Incorrect, but we will deal with that in other ways.)
    
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
    
    if consumed[index]:
        return None

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

def check_unconsumed(args: list[str], consumed: list[bool]):
    unconsumed: list[str] = []

    for (index, value) in enumerate(consumed):
        if not value:
            unconsumed.append(args[index])
    
    if len(unconsumed) > 0:
        print("Error: Unrecognized command line arguments.")
        print("The following command line inputs could not be interpreted: ", end="")
        print(str(unconsumed)[1:-1]) # Don't print the square brackets.
        print(f"Run 'python {args[0]} --help' to learn more.")
        sys.exit(1)

def str_to_size(string: str) -> int:
    """
    Uses a string to produce an integer size.
    A multiplier can be specified as a single character.

    Raises ValueError if an empty string is passed.
    Raises ValueError if the string can not be parsed.
    Raises KeyError if a bad multiplier is used.
    """

    if len(string) == 0:
        raise ValueError()

    suffix_start: int = 0

    while suffix_start < len(string) and string[suffix_start] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        suffix_start += 1
    
    value = int(string[:suffix_start])
    multiplier = 1

    if suffix_start < len(string):

        multiplier_dict = {
            "B": 1,
            "K": 2**10,
            "M": 2**20,
            "G": 2**30,
            "T": 2**40,
            "P": 2**50,
            "E": 2**60,
            "Y": 2**70,
            "Z": 2**80,
        }

        multiplier = multiplier_dict[string[suffix_start].upper()]
    
    return value * multiplier
