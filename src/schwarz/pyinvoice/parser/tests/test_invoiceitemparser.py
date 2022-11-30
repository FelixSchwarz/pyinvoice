# -*- coding: UTF-8 -*-

from schwarz.pyinvoice.model import InvoiceItem
from ..invoiceitemparser import InvoiceItemParser


def test_parse_invoice_item():
    xml = '<item price="-10.5" vat="0.10" number="3">   Moon </item>'
    read_item = InvoiceItemParser.parse(content=xml)
    assert read_item == InvoiceItem('Moon', -10.5, vat=0.10, number=3)

def test_parse_invoice_item_with_default_value():
    """Test that default values are set"""
    xml = '<item price="-10.5">   Moon </item>'
    read_item = InvoiceItemParser.parse(content=xml, default_vat=0.42)
    assert read_item == InvoiceItem('Moon', -10.5, vat=0.42, number=1)

