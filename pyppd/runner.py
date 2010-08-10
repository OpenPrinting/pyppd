import os
import stat
import errno
import logging
import logging.handlers
from optparse import OptionParser
import archiver

def parse_args():
    usage = "usage: %prog [options] ppds_directory"
    version = "%prog 0.4.1\n" \
              "Copyright (c) 2010 Vitor Baptista.\n" \
              "This is free software; see the source for copying conditions.\n" \
              "There is NO warranty; not even for MERCHANTABILITY or\n" \
              "FITNESS FOR A PARTICULAR PURPOSE."
    parser = OptionParser(usage=usage,
                          version=version)
    parser.add_option("-v", "--verbose",
                      action="store_const", const=1, dest="verbose",
                      help="run verbosely")
    parser.add_option("-d", "--debug",
                      action="store_const", const=2, dest="verbose",
                      help="print debug messages")
    parser.add_option("-o", "--output",
                      default="pyppd-ppdfile", metavar="FILE",
                      help="write archive to FILE [default %default]")
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("incorrect number of arguments")

    if not os.path.isdir(args[0]):
        parser.error("'%s' isn't a directory" % args[0])

    return (options, args)

def configure_logging(log_file, verbosity):
    """Configures logging to stdout and log_file

    To stdout, we only WARNING of worse messages in a simpler format. To the
    file, we save every log message with its time, level, module and method.
    We also rotate the log_file, removing old entries when it reaches 2 MB.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    console = logging.StreamHandler()
    if verbosity == 1:
        console.setLevel(logging.INFO)
    elif verbosity == 2:
        console.setLevel(logging.DEBUG)
    else:
        console.setLevel(logging.WARNING)

    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    console.setFormatter(formatter)
    logger.addHandler(console)

    handler = logging.handlers.RotatingFileHandler(log_file,
                    maxBytes=2*1024*1024)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] ' \
                                  '%(module)s.%(funcName)s(): %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def run():
    (options, args) = parse_args()
    configure_logging('pyppd.log', options.verbose)
    ppds_directory = args[0]
    
    logging.info('Archiving folder "%s".' % ppds_directory)
    archive = archiver.archive(ppds_directory)
    if not archive:
        exit(errno.ENOENT)

    logging.info('Writing archive to "%s".' % options.output)
    output = open(options.output, "w+")
    output.write(archive)
    output.close()

    logging.info('Setting "%s" executable flag.' % options.output)
    execute_mode = stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH
    mode = os.stat(options.output).st_mode | execute_mode
    os.chmod(options.output, mode)
