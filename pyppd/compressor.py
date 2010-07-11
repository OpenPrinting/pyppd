import os
import fnmatch
import sqlite3
from tempfile import NamedTemporaryFile
from ppd import PPD
import lzma_proxy as lzma

def find_files(directory, pattern):
    """Yields each file that matches pattern in directory."""
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, pattern):
            yield os.path.join(root, filename)

def compress(directory):
    """Compresses and indexes all *.ppd files in directory returning as a string.

    The directory is walked recursively, inserting all ppds found in a sqlite3 db.
    For each, it parses and saves its name, description (in the format CUPS needs)
    and the file.
    It returns the compressed dump of the sqlite3 database.

    """
    db_file = NamedTemporaryFile()
    con = sqlite3.connect(db_file.name)
    con.text_factory = str
    cur = con.cursor()
    cur.execute("CREATE TABLE ppds (name TEXT, description TEXT, file TEXT)")

    for ppd_path in find_files(directory, "*.ppd"):
        try:
            ppd_file = open(ppd_path).read()
            a_ppd = PPD(ppd_file)
            cur.execute("INSERT INTO ppds VALUES (?, ?, ?)",
                        (a_ppd.name, str(a_ppd), ppd_file))
        except:
            next

    con.commit()
    con.close()
    db_file.seek(0)
    ppds_compressed = lzma.compress(db_file.read())
    db_file.close()
    return ppds_compressed
