# -*- coding: UTF-8 -*-

from datetime import date as Date

from schwarz.pyinvoice.model import Address, Invoice, InvoiceItem
from ..invoiceparser import InvoiceParser


def generate_xml(extra_invoice_attribute='', *, date='30.02.2006'):
    xml = f"""<invoice invoiceSubject="Rechnung" invoiceDate="{date}" invoiceNumber="R001" defaultVat="0.42" {extra_invoice_attribute}>
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
    return xml


def test_parse_invoice():
    address = Address('FooBar Inc.', '9th Avenue', '12345', 'New York', [])
    itemA = InvoiceItem('Moon', 196, vat=0.42, number=3)
    itemB = InvoiceItem('Sun', -10.5, vat=0.10, number=2)
    items = [itemA, itemB]
    i = Invoice('30.02.2006', address, items, default_vat=0.42,
                invoice_number='R001', invoice_subject='Rechnung',
                note='Foobar')
    read_invoice = InvoiceParser.parse(content=generate_xml())
    assert read_invoice == i
    assert i.get_language() == Invoice.DEFAULT_LANGUAGE

def test_parse_invoice_with_language():
    actual_invoice = InvoiceParser.parse(content=generate_xml("language='en'"))
    assert actual_invoice.get_language() == 'en'

def test_can_parse_invoice_currency():
    invoice = InvoiceParser.parse(content=generate_xml('currency="USD"'))
    assert invoice.currency == 'USD'

def test_can_parse_invoice_date_as_date():
    invoice = InvoiceParser.parse(content=generate_xml(date='2023-06-01'))
    assert invoice.invoice_date == Date(2023, 6, 1)

