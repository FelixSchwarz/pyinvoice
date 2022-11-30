# -*- coding: UTF-8 -*-

from decimal import Decimal

from ..address import Address
from ..invoice import Invoice
from ..invoice_item import InvoiceItem


def test_invoice_equals():
    """Test that the custom equals function is working."""
    address = Address('Foo Bar', 'Bridge Street', '01234', 'City', ['a', 'b'])
    itemA = InvoiceItem('foo', 10, vat=0.10, number=2)
    itemB = InvoiceItem('bar', 100, vat=0.20, number=5)
    items = [itemA, itemB]
    a = Invoice(address, items, default_vat=0.42)
    b = Invoice(address, items, default_vat=0.42)
    assert a == a
    assert a == b
    assert not(a == Invoice(a, None))

def test_invoice_inequal():
    """Test that the custom ne function is working.."""
    address = Address('Foo Bar', 'Bridge Street', '01234', 'City', ['a', 'b'])
    itemA = InvoiceItem('foo', 10, vat=0.10, number=2)
    itemB = InvoiceItem('bar', 100, vat=0.20, number=5)
    items = [itemA, itemB]
    a = Invoice('01.01.2006', address, items)
    assert not (a != Invoice('01.01.2006', address, items))
    assert a is not None
    assert a != 'invalid'
    assert a != Invoice('01.01.2006', a, None)
    assert a != Invoice('01.01.2006', None, items)
    assert a != Invoice('01.01.2006', address, items, default_vat=0.2)
    assert a != Invoice('02.01.2006', address, items)
    assert a != Invoice('01.01.2006', address, items, invoice_number='R00012')
    assert a != Invoice('01.01.2006', address, items, invoice_subject='foo bar')
    assert a != Invoice('01.01.2006', address, items, note='foo')
    assert Invoice('01.01.2006', address, items, language='en') != a
    assert Invoice('01.01.2006', address, items, currency='USD') != a

def test_invoice_summing():
    """Test that all prices are summed correctly when ignoring vat."""
    itemA = InvoiceItem('foo', 10.333, vat=0.10, number=2)
    itemB = InvoiceItem('bar', 100, vat=0.20, number=5)
    itemC = InvoiceItem('foo', 50, vat=0.10, number=2)
    a = Invoice('01.01.2006', None, [itemA, itemB, itemC])
    assert a.get_real_sum(net=True) == Decimal('620.666')
    assert a.get_sum(net=True) == Decimal('620.67')

def test_invoice_summing_vat():
    """Test that all prices are summed correctly including the vat."""
    itemA = InvoiceItem('foo', 1.249, vat=0.10, number=2) # 2.7478
    itemB = InvoiceItem('bar', 1.5, vat=0.20, number=5) # 9
    itemC = InvoiceItem('foo', 5.0, vat=0.10, number=2) # 11
    a = Invoice('01.01.2006', None, [itemA, itemB, itemC])
    assert a.get_real_sum() == Decimal('22.7478')
    assert a.get_sum() == Decimal('22.75')

def test_invoice_summing_rounding():
    """Test that net sum + vat sums == brutto sum, even when rounding would give another sum."""
    itemA = InvoiceItem('foo', Decimal('0.803'), vat=Decimal('0.252801992528019925280199253'))
    # net is 0.803
    # vat sum is 0.203
    # brutto is 1.006
    # customer should get sum of 1.00 unless get_real_sum is used
    a = Invoice('', None, [itemA])
    assert a.get_sum(net=False) == Decimal('1.00')
    assert a.get_real_sum(net=False) == Decimal('1.006')

def test_invoice_vat_sums():
    """Test that vat sums are correctly calculated."""
    itemA = InvoiceItem('a', 10, vat=0.20)
    itemB = InvoiceItem('b', 10, vat=0.10, number=10)
    itemC = InvoiceItem('c', 10, vat=0.20)
    itemD = InvoiceItem('d', 10, vat=0)
    a = Invoice('', None, [itemA, itemB, itemC, itemD])
    vats = a.get_vat_sums()
    assert len(vats) == 3
    assert vats[0] == (Decimal('0'), Decimal('0'))
    assert vats[1] == (Decimal('0.10'), Decimal('10'))
    assert vats[2] == (Decimal('0.20'), Decimal('4'))

def test_invoice_vat_sums_rounding():
    """Test that vat sums are correctly calculated (with and without limitation
    to two numbers after decimal point)."""
    itemA = InvoiceItem('a', 10.333, vat=0.20)
    a = Invoice('', None, [itemA])

    vats = a.get_real_vat_sums()
    assert len(vats) == 1
    assert vats[0] == (Decimal('0.2'), Decimal('2.0666'))

    vats = a.get_vat_sums()
    assert len(vats) == 1
    assert vats[0] == (Decimal('0.2'), Decimal('2.07'))

def test_invoice_has_language():
    invoice = Invoice('', None)
    assert invoice.get_language() == Invoice.DEFAULT_LANGUAGE
    invoice = Invoice('', None, language='en')
    assert invoice.get_language() == 'en'

def test_invoice_has_currency():
    invoice = Invoice('', None)
    assert invoice.currency == 'EUR'
    invoice = Invoice('#', None, currency='USD')
    assert invoice.currency == 'USD'
