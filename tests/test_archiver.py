#!/usr/bin/env python3

import unittest
import tempfile
import os
import shutil
import base64
import json
import pyppd.archiver
import pyppd.compressor

class TestArchiver(unittest.TestCase):
    """Test the archiver module functionality."""
    
    def setUp(self):
        """Create a temporary directory with sample PPD files."""
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        
        # Create a sample PPD file
        self.ppd_content = b"""*LanguageVersion: English
*Manufacturer: "Test Manufacturer"
*NickName: "Test Printer"
*ModelName: "Test Model"
*Product: "(Test Printer)"
"""
        self.ppd_file = os.path.join(self.test_dir, "test.ppd")
        with open(self.ppd_file, "wb") as f:
            f.write(self.ppd_content)
        
        # Create a subdirectory with another PPD file
        os.makedirs(os.path.join(self.test_dir, "subdir"))
        self.ppd_file2 = os.path.join(self.test_dir, "subdir", "test2.ppd")
        with open(self.ppd_file2, "wb") as f:
            f.write(self.ppd_content)
    
    def tearDown(self):
        """Clean up the temporary directory."""
        shutil.rmtree(self.test_dir)
    
    def test_find_files(self):
        """Test finding PPD files in a directory."""
        ppd_files = list(pyppd.archiver.find_files(self.test_dir, ["*.ppd"]))
        
        # Check that we found both PPD files
        self.assertEqual(len(ppd_files), 2)
        self.assertIn(self.ppd_file, ppd_files)
        self.assertIn(self.ppd_file2, ppd_files)
    
    def test_compress(self):
        """Test compressing PPD files into an archive."""
        compressed = pyppd.archiver.compress(self.test_dir)
        
        # Check that compression worked
        self.assertIsNotNone(compressed)
        
        # Decompress and check the content
        decompressed = pyppd.compressor.decompress(compressed)
        ppds_index = json.loads(decompressed.decode('ASCII'))
        
        # Check that the archive contains our PPDs
        self.assertIn('ARCHIVE', ppds_index)
        self.assertEqual(len(ppds_index) - 1, 2)  # -1 for the ARCHIVE key
        
        # Check PPD URIs
        uris = [key for key in ppds_index.keys() if key != 'ARCHIVE']
        expected_uris = ['0/test.ppd', '0/subdir/test2.ppd']
        for uri in expected_uris:
            self.assertTrue(any(uri in found_uri for found_uri in uris))
    
    def test_archive(self):
        """Test creating an executable archive."""
        archive = pyppd.archiver.archive(self.test_dir)
        
        # Check that archive creation worked
        self.assertIsNotNone(archive)
        
        # Check that the archive contains the expected components
        self.assertIn(b"@compressor@", archive)
        self.assertIn(b"@ppds_compressed_b64@", archive)

if __name__ == '__main__':
    unittest.main()

