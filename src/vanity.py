import argparse

import license_explorer
from dmv import CA_DMV, CacheOption

parser = argparse.ArgumentParser(description="Searches for vanity license plates.")
parser.add_argument("input",
                    help="The seed for the search, something like BREAD")
parser.add_argument("-d", "--distance", type=int, default=3,
                    help="The maximum distance to search (3 by default)")
parser.add_argument("-w", "--output-width", type=int, default=10,
                    help="The maximum number of output per line in the output (10 by default)")
parser.add_argument("-m", "--max-length", type=int, default=7,
                    help="The maximum length of the outputs (7 by default)")
parser.add_argument("--dmv-test", dest="dmv_test", action="store_true",
                    help="if used, check the input against the CA DMV registry")
parser.add_argument("--cache", type=CacheOption.from_string, choices=list(CacheOption), default=CacheOption.DEFAULT,
                    help="Cache configuration, for debugging (memory and disk by default)")
args = parser.parse_args()

if (args.dmv_test):
    print("Is \"{}\" available as a CA DMV license plate?...".format(args.input))
    dmv = CA_DMV(args.cache)
    print(dmv.check_plate(args.input))
else:
    license_explorer.explore(args.input, args.distance, args.output_width, args.max_length)
