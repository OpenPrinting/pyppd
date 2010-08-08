import os
import stat
from optparse import OptionParser
import archiver

def parse_args():
    usage = "usage: %prog [options] ppds_directory"
    version = "%prog 0.2.2\n" \
              "Copyright (c) 2010 Vitor Baptista.\n" \
              "This is free software; see the source for copying conditions.\n" \
              "There is NO warranty; not even for MERCHANTABILITY or\n" \
              "FITNESS FOR A PARTICULAR PURPOSE."
    parser = OptionParser(usage=usage,
                          version=version)
    parser.add_option("-o", "--output",
                      default="pyppd-ppdfile", metavar="FILE",
                      help="write archive to FILE [default %default]")
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("incorrect number of arguments")

    if not os.path.isdir(args[0]):
        parser.error("'%s' isn't a directory" % args[0])

    return (options, args)


def run():
    (options, args) = parse_args()
    ppds_directory = args[0]

    archive = archiver.archive(ppds_directory)

    output = open(options.output, "w+")
    output.write(archive)
    output.close()

    execute_mode = stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH
    mode = os.stat(options.output).st_mode | execute_mode
    os.chmod(options.output, mode)
