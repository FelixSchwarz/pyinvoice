#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from decimal import Decimal

from ..invoice_item import InvoiceItem

def test_invoice_item_position_title():
    item = InvoiceItem('foo bar', item_price=2)
    assert item.get_title() is None
    assert item.get_subtext() == 'foo bar'

    item.name = 'foo // bar baz'
    assert item.get_title() == 'foo'
    assert item.get_subtext() == 'bar baz'

def test_invoice_item_get_real_price():
    """Test that Decimal computation is used."""
    item = InvoiceItem('foo', 2.333, number=2)
    assert item.get_real_price() == Decimal('4.666')

def test_invoice_item_get_price():
    """Test that prices have only two digits after the decimal point."""
    item = InvoiceItem('foo', 2.333, number=2)
    assert item.get_price() == Decimal('4.67')

    item = InvoiceItem('foo', 2.333, number=2, vat=0.5)
    assert item.get_price(net=True) == Decimal('4.67')

def test_invoice_item_get_real_price_vat():
    """Test that vat is added correctly."""
    item = InvoiceItem('foo', 10, vat=0.10)
    assert item.get_real_price() == Decimal('11')
    assert item.get_real_price(net=True) == Decimal('10')

    item = InvoiceItem('foo', 10, vat=0.50)
    assert item.get_real_price() == Decimal('15')
    assert item.get_real_price(net=True) == Decimal('10')

def test_invoice_item_get_vat():
    """Test that vat is computed correctly."""
    item = InvoiceItem('foo', 1, vat=0.10, number=10)
    assert item.get_vat() == Decimal('1')


def test_invoice_item_equals():
    """Test that the custom equals function is working.."""
    a = InvoiceItem('foo', 10, vat=0.10, number=2)
    b = InvoiceItem('foo', 10, vat=0.10, number=2)
    assert a == a
    assert a == b
    assert not (a == InvoiceItem('bar', 10, vat=0.10, number=2))

def test_invoice_item_inequal():
    """Test that the custom ne function is working.."""
    a = InvoiceItem('foo', 10, vat=0.10, number=2)
    assert not (a != InvoiceItem('foo', 10, vat=0.10, number=2))
    assert a != None
    assert a != 'invalid'
    assert a != InvoiceItem('bar', 10, vat=0.10, number=2)
    assert a != InvoiceItem('foo', 15, vat=0.10, number=2)
    assert a != InvoiceItem('foo', 10, vat=0.20, number=2)
    assert a != InvoiceItem('foo', 10, vat=0.10, number=4)

