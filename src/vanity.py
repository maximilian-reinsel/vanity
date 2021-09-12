import argparse

import license_explorer

parser = argparse.ArgumentParser(description="Searches for vanity license plates.")
parser.add_argument("input", 
                    help="The seed for the search, something like BREAD")
parser.add_argument("-d", "--distance", type=int, default=3, 
                    help="The maximum distance to search (3 by default)")

args = parser.parse_args()
license_explorer.explore(args.input, args.distance)