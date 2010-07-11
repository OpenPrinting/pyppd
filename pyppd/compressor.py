import os
import fnmatch
import cPickle
from ppd import PPD
import lzma_proxy as lzma

def find_files(directory, pattern):
    """Yields each file that matches pattern in directory."""
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, pattern):
            yield os.path.join(root, filename)

def compress(directory):
    """Compresses and indexes all *.ppd files in directory returning as a string.

    The directory is walked recursively, concatenating all ppds found. For each,
    it saves it's path, size and where it starts (in the concatenated strings)
    into a dictionary.
    Then, it compresses the string of all ppds concatenated and returns the
    pickle dump of the dictionary concatenated with the compressed ppds.

    """
    ppds = {}            # Dictionary with PPD objects.

    for ppd_path in find_files(directory, "*.ppd"):
        try:
            ppd_file = open(ppd_path).read()
            a_ppd = PPD(ppd_file)
            ppds[a_ppd.name] = (str(a_ppd), ppd_file)
        except:
            next

    ppds_pickle = cPickle.dumps(ppds)
    ppds = None
    ppds_compressed = lzma.compress(ppds_pickle)
    return ppds_compressed
