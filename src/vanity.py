import argparse

import license_explorer

parser = argparse.ArgumentParser(description="Searches for vanity license plates.")
parser.add_argument("input", 
                    help="The seed for the search, something like BREAD")
parser.add_argument("-d", "--distance", type=int, default=3, 
                    help="The maximum distance to search (3 by default)")
parser.add_argument("-w", "--output-width", type=int, default=10, 
                    help="The maximum number of output per line in the output (10 by default)")
parser.add_argument("-m", "--max-length", type=int, default=7, 
                    help="The maximum length of the outputs (7 by default)")

args = parser.parse_args()
license_explorer.explore(args.input, args.distance, args.output_width, args.max_length)