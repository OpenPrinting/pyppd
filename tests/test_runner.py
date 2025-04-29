#!/usr/bin/env python3

import unittest
import tempfile
import os
import sys
import shutil
from io import StringIO
import pyppd.runner

class TestRunner(unittest.TestCase):
    """Test the runner module functionality."""
    
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
        
        # Save original stdout and argv
        self.original_stdout = sys.stdout
        self.original_argv = sys.argv
        
        # Redirect stdout to capture output
        sys.stdout = StringIO()
    
    def tearDown(self):
        """Clean up temporary files and restore stdout."""
        shutil.rmtree(self.test_dir)
        
        # Restore stdout and argv
        sys.stdout = self.original_stdout
        sys.argv = self.original_argv
        
        # Remove the generated archive if it exists
        if os.path.exists("pyppd-ppdfile"):
            os.unlink("pyppd-ppdfile")
    
    def test_parse_args(self):
        """Test command-line argument parsing."""
        sys.argv = ['pyppd', self.test_dir]
        options, args = pyppd.runner.parse_args()
        
        # Check that the arguments were parsed correctly
        self.assertEqual(args[0], self.test_dir)
        self.assertEqual(options.output, "pyppd-ppdfile")
    
    def test_parse_args_with_output(self):
        """Test command-line argument parsing with output option."""
        output_file = "test-output"
        sys.argv = ['pyppd', '-o', output_file, self.test_dir]
        options, args = pyppd.runner.parse_args()
        
        # Check that the arguments were parsed correctly
        self.assertEqual(args[0], self.test_dir)
        self.assertEqual(options.output, output_file)
    
    def test_run(self):
        """Test running the command."""
        sys.argv = ['pyppd', '-o', 'test-output', self.test_dir]
        
        # Run the command
        pyppd.runner.run()
        
        # Check that the output file was created
        self.assertTrue(os.path.exists('test-output'))
        
        # Clean up the output file
        os.unlink('test-output')

if __name__ == '__main__':
    unittest.main()

