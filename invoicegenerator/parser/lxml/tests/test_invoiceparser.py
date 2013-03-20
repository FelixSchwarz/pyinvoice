#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

from invoicegenerator.model.address import Address
from invoicegenerator.model.invoice import Invoice
from invoicegenerator.model.invoice_item import InvoiceItem
from invoicegenerator.parser.lxml.invoiceparser import InvoiceParser

def generate_xml(additional_invoice_attribute=""):
    xml = """<?xml version="1.0" encoding='UTF-8'?>
<invoice invoiceSubject="Rechnung" invoiceDate="30.02.2006" invoiceNumber="R001" defaultVat="0.42" %s>
    <billingAddress>
       <name>FooBar Inc.</name>
       <street>9th Avenue</street>
       <zip>12345</zip>
       <city>New York</city>
    </billingAddress>
    
    <item price="196" number="3">
        Moon  
    </item>
    <item price="-10.5" vat="0.10" number="2">
        Sun
    </item>
    <note>Foobar</note>
</invoice>
"""
    return xml % additional_invoice_attribute

class TestInvoiceParser(unittest.TestCase):
    
    def test_parse(self):
        address = Address("FooBar Inc.", "9th Avenue", "12345", "New York", [])
        itemA = InvoiceItem("Moon", 196, vat=0.42, number=3)
        itemB = InvoiceItem("Sun", -10.5, vat=0.10, number=2)
        items = [itemA, itemB]
        i = Invoice("30.02.2006", address, items, default_vat=0.42,
                    invoice_number="R001", invoice_subject="Rechnung", 
                    note="Foobar")
        read_invoice = InvoiceParser.parse(content=generate_xml())
        self.assertEquals(i, read_invoice)
        self.assertEquals(Invoice.DEFAULT_LANGUAGE, i.get_language())
        
    def test_parse_with_language(self):
        actual_invoice = InvoiceParser.parse(content=generate_xml("language='en'"))
        self.assertEquals("en", actual_invoice.get_language())
    
    def test_can_parse_currency(self):
        invoice = InvoiceParser.parse(content=generate_xml('currency="USD"'))
        self.assertEquals('USD', invoice.currency)
    

if __name__ == "__main__":
    unittest.main()

