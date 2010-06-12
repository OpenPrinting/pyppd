import os
import fnmatch
import cPickle
import lzma

def find_files(directory, pattern):
    """Yields each file that matches pattern in directory"""
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, pattern):
            yield os.path.join(root, filename)

def compress(directory):
    ppds = ""            # String with all PPDs concatenated.
    ppds_size = 0        # Auxiliary value that holds intermediate ppds size.
    ppds_attributes = {} # Dictionary with each PPD start and size values in ppds.

    for ppd_path in find_files(directory, "*.ppd"):
        ppd = open(ppd_path).read()
        ppd_size = len(ppd)
        ppd_start = ppds_size
        ppds_size += ppd_size
        ppds_attributes[ppd_path] = {"start": ppd_start, "size": ppd_size}
        ppds += ppd

    ppds_compressed = lzma.compress(ppds)
    return cPickle.dumps(ppds_attributes) + ppds_compressed
