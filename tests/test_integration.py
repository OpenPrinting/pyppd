#!/usr/bin/env python3

import unittest
import tempfile
import os
import subprocess
import shutil
import sys

class TestIntegration(unittest.TestCase):
    """Test the full integration workflow."""
    
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
    
    def tearDown(self):
        """Clean up temporary files."""
        shutil.rmtree(self.test_dir)
        
        # Remove the generated archive if it exists
        if os.path.exists("pyppd-ppdfile"):
            os.unlink("pyppd-ppdfile")
    
    def test_full_workflow(self):
        """Test the full workflow from creation to extraction."""
        # Create the archive
        subprocess.run([sys.executable, "-m", "bin.pyppd", self.test_dir],
                      check=True, capture_output=True)
        
        # Check that the archive was created
        self.assertTrue(os.path.exists("pyppd-ppdfile"))
        self.assertTrue(os.access("pyppd-ppdfile", os.X_OK))
        
        # List the PPDs in the archive
        list_result = subprocess.run(["./pyppd-ppdfile", "list"],
                                    check=True, capture_output=True)
        self.assertIn(b"pyppd-ppdfile:test.ppd", list_result.stdout)
        
        # Extract a PPD from the archive
        cat_result = subprocess.run(["./pyppd-ppdfile", "cat", "pyppd-ppdfile:test.ppd"],
                                   check=True, capture_output=True)
        self.assertEqual(cat_result.stdout, self.ppd_content)
    
    def test_rename_workflow(self):
        """Test renaming the archive and using it."""
        # Create the archive
        subprocess.run([sys.executable, "-m", "bin.pyppd", self.test_dir],
                      check=True, capture_output=True)
        
        # Rename the archive
        os.rename("pyppd-ppdfile", "renamed-archive")
        
        # List the PPDs in the renamed archive
        list_result = subprocess.run(["./renamed-archive", "list"],
                                    check=True, capture_output=True)
        self.assertIn(b"renamed-archive:test.ppd", list_result.stdout)
        
        # Extract a PPD from the renamed archive
        cat_result = subprocess.run(["./renamed-archive", "cat", "renamed-archive:test.ppd"],
                                   check=True, capture_output=True)
        self.assertEqual(cat_result.stdout, self.ppd_content)
        
        # Clean up the renamed archive
        os.unlink("renamed-archive")

if __name__ == '__main__':
    unittest.main()

