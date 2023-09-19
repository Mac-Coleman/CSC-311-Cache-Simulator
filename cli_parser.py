"""
Written by Mac
"""

from enum import Enum
import sys
from typing import cast, Callable, TypedDict

class OptionFormat(Enum):
    COMBINED_SHORT = 0
    COMBINED_LONG = 1
    SEPARATE_SHORT = 2
    SEPARATE_LONG = 3

class OptionDict(TypedDict):
    cache_type: str
    memory_size: int
    block_size: int
    cache_size: int
    reads: int
    no_color: bool
    k: int
    replacement: str
    access_pattern: str
    quiet: bool
    probability: float
    output_disabled: bool

number_help = "NUMBER INTERPRETATION:\n" \
    "\tNumbers can be passed on the command line as either\n" \
    "\tinteger literals or with SI multipliers. You can\n" \
    "\tspecify a number by writing out all of its digits,\n" \
    "\tor by writing a number with a multiplier suffix.\n\n" \
    "EXAMPLES:\n" \
    "\t256  -> 256\n" \
    "\t512B -> 512\n" \
    "\t256K -> 262144\n" \
    "\t  1G -> 1073741823\n"

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

    memory_size = str_to_size("256MB")
    block_size = str_to_size("4KB")
    cache_size = str_to_size("32KB")
    replacement = "lru"
    access_pattern = "random"
    probability = 0.35

    run_help = get_flag_presence(args, consumed, "--help", "-h")
    run_version = get_flag_presence(args, consumed, "--version", "-v")

    if run_help:
        help_handler(file_name)
        return
    
    if run_version:
        version_handler(file_name)
        return


    try:
        memory_size_parsed = get_option_value(args, consumed, "--memory-size", "-m")
        block_size_parsed = get_option_value(args, consumed, "--block-size", "-b")
        cache_size_parsed = get_option_value(args, consumed, "--cache-size", "-c")
        k_parsed = get_option_value(args, consumed, "--ways", "-k")
        replacement_parsed = get_option_value(args, consumed, "--replacement", "-r")
        access_pattern_parsed = get_option_value(args, consumed, "--access-pattern", "-a")
        probability_parsed = get_option_value(args, consumed, "--probability", "-p")

        no_colorize = get_flag_presence(args, consumed, "--no-color", "-n")
        quiet = get_flag_presence(args, consumed, "--quiet", "-q")
        disable_output = get_flag_presence(args, consumed, "--disable-output-files", "-d")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Unconsumed arguments are positionals.
    positionals: list[str] = []

    count = 0
    for i in range(len(args)):
        if not consumed[i]:
            positionals.append(args[i])
        
            if count < 2:
                consumed[i] = True
                count += 1
    
    if len(positionals) != 2:
        print("Error: Cache simulator requires exactly two positional arguments.\n")
        print("Arguments:")
        print("\tTYPE    The type of cache mapping to use.")
        print("\tREADS   The number of reads to perform.")
        print("Run again with the -h or --help options to learn more.")
        sys.exit(1)



    if memory_size_parsed:
        try:
            memory_size = str_to_size(memory_size_parsed)
        except:
            print("Error: Could not correctly interpret memory size.\n")
            print(number_help)
            sys.exit(1)
    
    if block_size_parsed:
        try:
            block_size = str_to_size(block_size_parsed)
        except:
            print("Error: Could not correctly interpret block size.\n")
            print(number_help)
            sys.exit(1)
    
    if cache_size_parsed:
        try:
            cache_size = str_to_size(cache_size_parsed)
        except:
            print("Error: Could not correctly interpret cache size.\n")
            print(number_help)
            sys.exit(1)

    cache_type = positionals[0].lower()
    reads = 0
    
    try:
        reads = str_to_size(positionals[1])
    except ValueError as e:
        print(f"Error: could not interpret number of reads: {positionals[1]}")
        print(number_help)
        sys.exit(1)
    except KeyError as e:
        print(f"Error: could not interpret number of reads: {positionals[1]}")
        print(number_help)
        sys.exit(1)

    type_dict: dict[str, str] = {
        "direct": "direct",
        "d": "direct",
        "1": "direct",
        "associative": "associative",
        "a": "associative",
        "2": "associative",
        "set-associative": "set-associative",
        "set_associative": "set-associative",
        "s": "set-associative",
        "3": "set-associative"
    }

    try:
        cache_type = type_dict[cache_type]
    except KeyError:
        print(f"Error: Unrecognized cache type: {cache_type}")
        sys.exit(1)
    
    if cache_type != "set-associative" and k_parsed is not None:
        print("Error: set size can only be specified for set-associative caches!")
        print("You must remove the --ways or -k options, or switch to a different cache type.")
        sys.exit(1)
    
    if cache_type == "set-associative" and k_parsed is None:
        print("Error: set size is required when using a set-associative cache!")
        print("You must add the --ways or -k flag, or switch to a different type of cache.")
        sys.exit(1)
    
    if replacement_parsed is not None and cache_type == "direct":
        print("Error: No replacement algorithm can be specified when using a direct cache!")
        print("You must remove the -r or --replacement options, or switch to a different cache type.")
        sys.exit(1)
    
    replacement_types = ["lru", "lfu", "fifo", "random"]
    
    if replacement_parsed is not None:
        if replacement_parsed.lower() in replacement_types:
            replacement = replacement_parsed.lower()
        else:
            print(f"Error: Replacement algorithm unrecognized: '{replacement_parsed}'\n")
            print("REPLACEMENT ALGORITHMS:")
            print("\tlru\tleast recently used")
            print("\tlfu\tleast frequently used")
            print("\tfifo\tfirst in first out")
            print("\trandom\trandom")
            sys.exit(1)
    
    access_patterns = ["random", "full-sequential", "random-pages", "probability", "random-sequential"]

    if access_pattern_parsed is not None:
        if access_pattern_parsed.lower() in access_patterns or access_pattern_parsed.lower().endswith(".log"):
            access_pattern = access_pattern_parsed.lower()
        else:
            print(f"Error: access pattern unrecognized: '{access_pattern_parsed}'\n")
            print("ACCESS PATTERNS:")
            print("\trandom\t\t\tgenerate random addresses within memory")
            print("\tfull-sequential\t\tread the entire address space sequentially")
            print("\trandom-sequential\tread from a random address to a random address sequentially")
            print("\trandom-pages\t\tread the address space of randomly selected pages")
            print("\tprobability\t\tread the memory with a certain probability of switching pages")
            print("\t\t\t\trequires the --probability option.")
            print("\t<file-name>\t\ta Valgrind Lackey .log file containing memory accesses by a process")
            sys.exit(1)
    
    if access_pattern == "probability" and probability_parsed is None:
        print("Error: probability was not provided.")
        print("When running with probability as the access mode, the --probability option must be specified.")
        print("Add the probability option or choose a different access pattern.")
        sys.exit(1)
    
    if access_pattern != "probability" and probability_parsed is not None:
        print("Error: probability was provided but access pattern does not support probability.")
        print("The --probability or -p option may not be specified with this access pattern.")
        print("Remove the probability option or choose a different access pattern.")
        sys.exit(1)

    if probability_parsed is not None:
        try:
            probability = float(probability_parsed)
        except ValueError:
            print("Error: Probability must be a floating-point number between one and zero.")
            sys.exit(1)
        
        if probability < 0 or probability > 1:
            print("Error: Probability must be a floating-point number between one and zero.")
            sys.exit(1)

    check_unconsumed(args, consumed)

    options: OptionDict = {
        "cache_type": cache_type,
        "memory_size": memory_size,
        "block_size": block_size,
        "cache_size": cache_size,
        "reads": reads,
        "no_color": no_colorize,
        "k": 0,
        "replacement": replacement,
        "quiet": quiet,
        "access_pattern": access_pattern,
        "probability": probability,
        "output_disabled": disable_output
    }

    if k_parsed is not None:
        try:
            options["k"] = int(k_parsed)
        except ValueError:
            print("Error: Set size could not be interpreted as an integer.")
            sys.exit(1)

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
    Consumes elements from args by marking them as consumed when they are found.
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
        raise ValueError(f"Option {args[option_style[1]]} was given but no value was specified.")
    
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
        raise ValueError("No value was found before the multiplier.")

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
