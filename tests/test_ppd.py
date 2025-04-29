#!/usr/bin/env python3

import unittest
import tempfile
import os
import pyppd.ppd

class TestPPD(unittest.TestCase):
    """Test the PPD parsing functionality."""
    
    def test_parse_basic_ppd(self):
        """Test parsing of a basic PPD file."""
        ppd_content = b"""*LanguageVersion: English
*Manufacturer: "Test Manufacturer"
*NickName: "Test Printer"
*ModelName: "Test Model"
*Product: "(Test Printer)"
"""
        filename = "test.ppd"
        parsed = pyppd.ppd.parse(ppd_content, filename)
        
        # Check that we got one PPD
        self.assertEqual(len(parsed), 1)
        
        # Check that the PPD has the correct attributes
        ppd = parsed[0]
        self.assertEqual(ppd.uri, "0/test.ppd")
        self.assertEqual(ppd.language, "en")
        self.assertEqual(ppd.manufacturer, "Test Manufacturer")
        self.assertEqual(ppd.nickname, "Test Printer")
    
    def test_parse_ppd_with_device_id(self):
        """Test parsing of a PPD file with a device ID."""
        ppd_content = b"""*LanguageVersion: English
*Manufacturer: "Test Manufacturer"
*NickName: "Test Printer"
*ModelName: "Test Model"
*1284DeviceID: "MFG:Test Manufacturer;MDL:Test Printer;"
"""
        filename = "test.ppd"
        parsed = pyppd.ppd.parse(ppd_content, filename)
        
        # Check that we got one PPD
        self.assertEqual(len(parsed), 1)
        
        # Check that the PPD has the correct attributes
        ppd = parsed[0]
        self.assertEqual(ppd.deviceid, "MFG:Test Manufacturer;MDL:Test Printer;")
    
    def test_parse_ppd_with_multiple_products(self):
        """Test parsing of a PPD file with multiple products."""
        ppd_content = b"""*LanguageVersion: English
*Manufacturer: "Test Manufacturer"
*NickName: "Test Printer"
*ModelName: "Test Model"
*Product: "(Test Printer 1)"
*Product: "(Test Printer 2)"
"""
        filename = "test.ppd"
        parsed = pyppd.ppd.parse(ppd_content, filename)
        
        # Check that we got two PPDs
        self.assertEqual(len(parsed), 2)
        
        # Check that the PPDs have the correct attributes
        self.assertEqual(parsed[0].uri, "0/test.ppd")
        self.assertEqual(parsed[1].uri, "1/test.ppd")
    
    def test_parse_gzipped_ppd(self):
        """Test parsing of a gzipped PPD file."""
        import gzip
        
        ppd_content = b"""*LanguageVersion: English
*Manufacturer: "Test Manufacturer"
*NickName: "Test Printer"
*ModelName: "Test Model"
*Product: "(Test Printer)"
"""
        # Create a temporary gzipped file
        with tempfile.NamedTemporaryFile(suffix='.ppd.gz', delete=False) as f:
            with gzip.open(f.name, 'wb') as gz:
                gz.write(ppd_content)
            filename = f.name
        
        try:
            # Load the file and parse it
            with gzip.open(filename, 'rb') as gz:
                content = gz.read()
            
            parsed = pyppd.ppd.parse(content, os.path.basename(filename)[:-3])
            
            # Check that we got one PPD
            self.assertEqual(len(parsed), 1)
            
            # Check that the PPD has the correct attributes
            ppd = parsed[0]
            self.assertEqual(ppd.manufacturer, "Test Manufacturer")
            self.assertEqual(ppd.nickname, "Test Printer")
        finally:
            os.unlink(filename)

if __name__ == '__main__':
    unittest.main()

