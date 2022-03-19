import argparse
import logging

import license_explorer
from dmv import CA_DMV, CacheOption

logger = logging.getLogger("vanity")

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
log_mode = parser.add_mutually_exclusive_group()
log_mode.add_argument("--debug", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.WARNING,
                    help="Enable debug logs")
log_mode.add_argument("-v", "--verbose", action="store_const", dest="loglevel", const=logging.INFO, default=logging.WARNING,
                    help="Enable verbose (informational) logs")
args = parser.parse_args()

FORMAT = '[%(name)s][%(levelname).1s] %(message)s'
logging.basicConfig(format=FORMAT, level=args.loglevel)
logger.info("Logging with level: %s", logging.getLevelName(args.loglevel))

if (args.dmv_test):
    print("Is \"{}\" available as a CA DMV license plate?...".format(args.input))
    dmv = CA_DMV(args.cache)
    print(dmv.check_plate(args.input))
else:
    license_explorer.explore(args.input, args.distance, args.output_width, args.max_length)
