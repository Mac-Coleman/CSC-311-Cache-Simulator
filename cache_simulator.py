"""
The top-level organization for the main program logic.
This will orchestrate the simulator and its components.
"""

from cli_parser import parse_arguments

import sys

def main():
    parse_arguments(sys.argv, run_help, run_version, run_simulator)

def run_version(executing_file: str):
    print("Version")

def run_help(executing_file: str):
    print("Help")

def run_simulator(options: dict[str, int]):
    print("Simulator")


if __name__ == "__main__":
    main()