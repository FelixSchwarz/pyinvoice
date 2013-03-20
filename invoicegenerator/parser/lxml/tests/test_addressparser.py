#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

from invoicegenerator.model.address import Address
from invoicegenerator.parser.lxml.addressparser import AddressParser

class TestAddressParser(unittest.TestCase):
    
    def test_parse(self):
        xml = """<billingAddress>
            <name>FooBar Inc.</name>
            <street>9th Avenue</street>
            <zip>12345</zip>
            <city>New York</city>
        </billingAddress>"""
        address = Address("FooBar Inc.", "9th Avenue", "12345", "New York", [])
        read_address = AddressParser.parse(content=xml)
        self.assertEquals(address, read_address)

if __name__ == "__main__":
    unittest.main()

