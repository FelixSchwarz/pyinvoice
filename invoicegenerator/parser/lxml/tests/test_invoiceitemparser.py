#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

from invoicegenerator.model.invoice_item import InvoiceItem
from invoicegenerator.parser.lxml.invoiceitemparser import InvoiceItemParser

class TestInvoiceItemParser(unittest.TestCase):
    
    def test_parse(self):
        xml = '<item price="-10.5" vat="0.10" number="3">   Moon </item>'
        read_item = InvoiceItemParser.parse(content=xml)
        item = InvoiceItem("Moon", -10.5, vat=0.10, number=3)
        self.assertEquals(item, read_item)
        
    def test_parse_defaults(self):
        """Test that default values are set"""
        xml = '<item price="-10.5">   Moon </item>'
        read_item = InvoiceItemParser.parse(content=xml, default_vat=0.42)
        item = InvoiceItem("Moon", -10.5, vat=0.42, number=1)
        self.assertEquals(item, read_item)

if __name__ == "__main__":
    unittest.main()

