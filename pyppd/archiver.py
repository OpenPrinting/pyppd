import base64
import sys
import os
import fnmatch
import gzip
import logging
from pathlib import Path
import json

import pyppd.compressor
import pyppd.ppd

try:
    # Python 3.9+ standard library
    from importlib.resources import files as resource_files
except ImportError:
    # Backport for Python <3.9
    try:
        from importlib_resources import files as resource_files
    except ImportError:
        resource_files = None  # Handle development environment fallback

def archive(ppds_directory):
    """Returns executable archive with decompressor and compressed PPDs."""
    # Compression logic
    ppds_compressed = compress(ppds_directory)
    
    # Read template
    template_path = Path(__file__).parent / "pyppd-ppdfile.in"
    with open(template_path, "rb") as f:
        template = f.read()
    
    # Read compressor code
    compressor_py = read_file_in_syspath("compressor.py")
    
    # Perform substitutions
    ppds_compressed_b64 = base64.b64encode(ppds_compressed)
    return template.replace(b"@compressor@", compressor_py)\
                  .replace(b"@ppds_compressed_b64@", ppds_compressed_b64)

def read_file_in_syspath(filename):
    """Read package resources with fallback for development environments."""
    try:
        if resource_files:
            return (resource_files('pyppd') / filename).read_bytes()
    except (ImportError, FileNotFoundError):
        pass

    # Fallback for development environment
    try:
        package_dir = Path(__file__).parent
        target_path = package_dir / filename
        return target_path.read_bytes()
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Could not find required file '{filename}' in package resources "
            f"or development path: {target_path}"
        )

def compress(directory):
    """Compress and index PPD files with proper resource handling."""
    ppds = bytearray()
    ppds_index = {}
    abs_directory = Path(directory).absolute()

    for ppd_path in sorted(find_files(directory, ("*.ppd", "*.ppd.gz"))):
        ppd_filename = str(ppd_path.relative_to(abs_directory))

        # Handle gzipped PPDs
        if ppd_path.suffix.lower() == '.gz':
            with gzip.open(ppd_path, 'rb') as f:
                ppd_file = f.read()
            ppd_filename = ppd_filename[:-3]  # Remove .gz extension
        else:
            with ppd_path.open('rb') as f:
                ppd_file = f.read()

        start = len(ppds)
        length = len(ppd_file)
        logging.debug(f'Found {ppd_path} ({length} bytes)')

        # Parse PPD and add to index
        ppd_parsed = pyppd.ppd.parse(ppd_file, ppd_filename)
        ppd_descriptions = [str(p) for p in ppd_parsed]
        
        for p in ppd_parsed:
            ppds_index[p.uri] = (start, length, ppd_descriptions)
        
        ppds.extend(ppd_file)

    if not ppds:
        logging.error(f'No PPDs found in directory: {directory}')
        return None

    # Compress and encode archive
    ppds_index['ARCHIVE'] = base64.b64encode(
        pyppd.compressor.compress(ppds)
    ).decode('ascii')
    
    return pyppd.compressor.compress(
        json.dumps(ppds_index, ensure_ascii=True, sort_keys=True).encode('utf-8')
    )

def find_files(directory, patterns):
    """Yield files matching patterns in directory hierarchy."""
    abs_directory = Path(directory).absolute()
    for path in abs_directory.rglob('*'):
        if path.is_file() and any(fnmatch.fnmatch(path.name, p) for p in patterns):
            yield path
