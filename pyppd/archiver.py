import base64
import sys

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

def create_archive(ppds_compressed):
    """Returns a string with the decompressor, its dependencies and the archive.

    It reads the template at pyppd/pyppd-ppdfile.in, inserts the dependencies
    and the archive encoded in base64, and returns as a string.

    """
    ppds_compressed = base64.b64encode(ppds_compressed)

    template = read_file_in_syspath("pyppd/pyppd-ppdfile.in")
    lzma_proxy_py = read_file_in_syspath("pyppd/lzma_proxy.py")

    template = template.replace("@lzma_proxy@", lzma_proxy_py)
    template = template.replace("@ppds_compressed_b64@", ppds_compressed)

    return template
