#!/usr/bin/env python3

import unittest
import tempfile
import os
import subprocess
import shutil
import sys

class TestCLI(unittest.TestCase):
    """Test the command-line interface."""
    
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
    
    def test_cli_basic(self):
        """Test basic CLI functionality."""
        result = subprocess.run(
            ["bin/pyppd", self.test_dir],  # Direct script execution
            check=True,
            capture_output=True
        )
        
        # Check that the output file was created
        self.assertTrue(os.path.exists("pyppd-ppdfile"))
        self.assertTrue(os.access("pyppd-ppdfile", os.X_OK))
    
    def test_cli_with_output(self):
        """Test CLI with custom output file."""
        output_file = "custom-output"
        
        # Run the pyppd command
        result = subprocess.run(
            ["bin/pyppd", "-o", output_file, self.test_dir],
            check=True,
            capture_output=True
        )
        
        # Check that the output file was created
        self.assertTrue(os.path.exists(output_file))
        self.assertTrue(os.access(output_file, os.X_OK))
        
        # Clean up the output file
        os.unlink(output_file)
    
    def test_cli_verbose(self):
        """Test CLI with verbose output."""
        # Run the pyppd command with verbose flag
        result = subprocess.run(
            ["bin/pyppd", "-v", self.test_dir],
            check=True,
            capture_output=True
        )
        
        # Check that the output file was created
        self.assertTrue(os.path.exists("pyppd-ppdfile"))
        
        # Check for verbose output
        self.assertIn(b"Compressing folder", result.stdout)

if __name__ == '__main__':
    unittest.main()
