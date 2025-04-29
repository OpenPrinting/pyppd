#!/usr/bin/env python3

import unittest
import tempfile
import os
import pyppd.compressor

class TestCompressor(unittest.TestCase):
    """Test the compressor module functionality."""
    
    def test_compress_decompress(self):
        """Test that data can be compressed and decompressed correctly."""
        test_data = b"Hello, World! This is test data for compression."
        compressed = pyppd.compressor.compress(test_data)
        
        # Check that compression actually happened
        self.assertLess(len(compressed), len(test_data))
        
        # Check that decompression restores the original data
        decompressed = pyppd.compressor.decompress(compressed)
        self.assertEqual(test_data, decompressed)
    
    def test_compress_file(self):
        """Test that a file can be compressed correctly."""
        test_data = b"This is test data for file compression."
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(test_data)
            filename = f.name
        
        try:
            # Compress the file
            compressed = pyppd.compressor.compress_file(filename)
            
            # Check that compression actually happened
            self.assertIsNotNone(compressed)
            self.assertLess(len(compressed), len(test_data))
            
            # Check that the compressed data can be decompressed
            decompressed = pyppd.compressor.decompress(compressed)
            self.assertEqual(test_data, decompressed)
        finally:
            os.unlink(filename)

if __name__ == '__main__':
    unittest.main()

