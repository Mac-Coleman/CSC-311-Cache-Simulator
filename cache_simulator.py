"""
The top-level organization for the main program logic.
This will orchestrate the simulator and its components.
"""

from cli_parser import parse_arguments

import sys

def main():
    arguments = parse_arguments(sys.argv)

if __name__ == "__main__":
    main()