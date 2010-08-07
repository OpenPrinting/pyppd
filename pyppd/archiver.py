import base64
import sys
import os
import fnmatch
import cPickle
import gzip
import compressor
from ppd import PPD

def archive(ppds_directory):
    """Returns a string with the decompressor, its dependencies and the archive.

    It reads the template at pyppd/pyppd-ppdfile.in, inserts the dependencies
    and the archive encoded in base64, and returns as a string.

    """
    ppds_compressed = base64.b64encode(compress(ppds_directory))

    template = read_file_in_syspath("pyppd/pyppd-ppdfile.in")
    compressor_py = read_file_in_syspath("pyppd/compressor.py")

    template = template.replace("@compressor@", compressor_py)
    template = template.replace("@ppds_compressed_b64@", ppds_compressed)

    return template

def compress(directory):
    """Compresses and indexes *.ppd and *.ppd.gz in directory returning a string.

    The directory is walked recursively, concatenating all ppds found in a string.
    For each, it tests if its filename ends in *.gz. If so, opens with gzip. If
    not, opens directly. Then, it parses and saves its name, description (in the
    format CUPS needs) and it's position in the ppds string (start position and
    length) into a dictionary, used as an index.
    Then, it compresses the string, adds into the dictionary as key ARCHIVE and
    returns a compressed pickle dump of it.

    """
    ppds = ""
    ppds_index = {}

    for ppd_path in find_files(directory, ("*.ppd", "*.ppd.gz")):
        if ppd_path.lower().endswith(".gz"):
            ppd_file = gzip.open(ppd_path).read()
        else:
            ppd_file = open(ppd_path).read()

        a_ppd = PPD(ppd_file)
        start = len(ppds)
        length = len(ppd_file)
        ppds_index[a_ppd.name] = (start, length, str(a_ppd))

        ppds += ppd_file

    ppds_index['ARCHIVE'] = compressor.compress(ppds)
    ppds_pickle = compressor.compress(cPickle.dumps(ppds_index))

    return ppds_pickle


def read_file_in_syspath(filename):
    """Reads the file in filename in each sys.path.

    If we couldn't find, throws the last IOError caught.

    """
    last_exception = None
    for path in sys.path:
        try:
            return open(path + "/" + filename).read()
        except IOError as ex:
            last_exception = ex
            continue
    raise last_exception

def find_files(directory, patterns):
    """Yields each file that matches any of patterns in directory."""
    abs_directory = os.path.abspath(directory)
    for root, dirnames, filenames in os.walk(abs_directory):
        for pattern in patterns:
            for filename in fnmatch.filter(filenames, pattern):
                yield os.path.join(root, filename)
