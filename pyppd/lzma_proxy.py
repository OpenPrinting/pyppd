from subprocess import Popen, PIPE
try:
    import lzma
except ImportError:
    try:
        Popen(["xz", "--version"], stdout=PIPE)
        binary = "xz"
    except OSError:
        raise OSError("Couldn't find neither python-lzma or the xz binary.")

def compress(value):
    """Compresses a string with either python-lzma or the xz binary"""
    if lzma:
        return lzma.compress(value)

    process = Popen([binary, "--compress", "--force"], stdin=PIPE, stdout=PIPE)
    return process.communicate(value)[0]

def decompress(value):
    """Decompresses a string with either python-lzma or the xz binary"""
    if lzma:
        return lzma.decompress(value)

    process = Popen([binary, "--decompress", "--stdout", "--force"],
                    stdin=PIPE, stdout=PIPE)
    return process.communicate(value)[0]
