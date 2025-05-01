import os
import stat
import errno
import logging
import sys
from optparse import OptionParser
import pyppd.archiver

def parse_args():
    usage = "usage: %prog [options] ppds_directory"
    version = "%prog 1.1.1\n" \
              "Copyright (c) 2013 Vitor Baptista.\n" \
              "This is free software; see the source for copying conditions.\n" \
              "There is NO warranty; not even for MERCHANTABILITY or\n" \
              "FITNESS FOR A PARTICULAR PURPOSE."
    parser = OptionParser(usage=usage, version=version)
    parser.add_option("-v", "--verbose",
                      action="count", dest="verbosity", default=0,
                      help="Increase verbosity level (up to -vv for debug)")
    parser.add_option("-o", "--output",
                      default="pyppd-ppdfile", metavar="FILE",
                      help="Write archive to FILE [default: %default]")
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("Incorrect number of arguments")
    if not os.path.isdir(args[0]):
        parser.error(f"'{args[0]}' is not a directory")

    return (options, args)

def configure_logging(verbosity):
    """Configure logging based on verbosity level"""
    level = logging.WARNING
    if verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG

    # Configure logging to stdout with simple format
    logging.basicConfig(
        level=level,
        format='%(message)s',
        stream=sys.stdout
    )

def run():
    (options, args) = parse_args()
    configure_logging(options.verbosity)
    ppds_directory = args[0]

    logging.info(f'Compressing folder "{ppds_directory}"')
    archive = pyppd.archiver.archive(ppds_directory)
    if not archive:
        exit(errno.ENOENT)

    logging.info(f'Writing archive to "{options.output}"')
    with open(options.output, "wb") as f:
        f.write(archive)

    logging.debug(f'Setting executable permissions on "{options.output}"')
    os.chmod(options.output, os.stat(options.output).st_mode | stat.S_IEXEC)

if __name__ == "__main__":
    run()
