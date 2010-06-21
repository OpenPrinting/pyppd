from optparse import OptionParser
from os.path import isdir
import compressor

def parse_args():
    parser = OptionParser(usage="usage: %prog [options] ppds_directory",
                          version="%prog 0.1.0\n"
                                  "Copyright (C) 2010 Vitor Baptista.\n"
                                  "This is free software; see the source for copying conditions.\n"
                                  "There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.")
    parser.add_option("-o", "--output",
                      default="ppds.pkl", metavar="FILE",
                      help="write archive to FILE [default %default]")
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("incorrect number of arguments")

    ppds_directory = args[0]
    if not isdir(ppds_directory):
        parser.error(ppds_directory + " isn't a directory")

    return (options, args)


def run():
    (options, args) = parse_args()

    output = open(options.output, "wb")
    output.write(compressor.compress(ppds_directory))
    output.close()
