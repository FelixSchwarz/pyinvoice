#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from decimal import Decimal
import unittest

from invoicegenerator.lib.pythonic_testcase import *
from invoicegenerator.model.address import Address
from invoicegenerator.model.invoice import Invoice
from invoicegenerator.model.invoice_item import InvoiceItem

class TestInvoice(PythonicTestCase):

    def test_equals(self):
        """Test that the custom equals function is working."""
        address = Address("Foo Bar", "Bridge Street", "01234", "City", ["a", "b"])
        itemA = InvoiceItem("foo", 10, vat=0.10, number=2)
        itemB = InvoiceItem("bar", 100, vat=0.20, number=5)
        items = [itemA, itemB]
        a = Invoice(address, items, default_vat=0.42)
        b = Invoice(address, items, default_vat=0.42)
        assert_equals(a, a)
        assert_equals(a, b)
        assert_false(a == Invoice(a, None))

    def test_inequal(self):
        """Test that the custom ne function is working.."""
        address = Address("Foo Bar", "Bridge Street", "01234", "City", ["a", "b"])
        itemA = InvoiceItem("foo", 10, vat=0.10, number=2)
        itemB = InvoiceItem("bar", 100, vat=0.20, number=5)
        items = [itemA, itemB]
        a = Invoice("01.01.2006", address, items)
        assert_false(a != Invoice("01.01.2006", address, items))
        assert_not_none(a)
        assert_not_equals(a, "invalid")
        assert_not_equals(a, Invoice("01.01.2006", a, None))
        assert_not_equals(a, Invoice("01.01.2006", None, items))
        assert_not_equals(a, Invoice("01.01.2006", address, items, default_vat=0.2))
        assert_not_equals(a, Invoice("02.01.2006", address, items))
        assert_not_equals(a, Invoice("01.01.2006", address, items, invoice_number="R00012"))
        assert_not_equals(a, Invoice("01.01.2006", address, items, invoice_subject="foo bar"))
        assert_not_equals(a, Invoice("01.01.2006", address, items, note="foo") )
        assert_not_equals(Invoice("01.01.2006", address, items, language='en'), a)
        assert_not_equals(Invoice("01.01.2006", address, items, currency='USD'), a)

    def test_summing(self):
        """Test that all prices are summed correctly when ignoring vat."""
        itemA = InvoiceItem("foo", 10.333, vat=0.10, number=2)
        itemB = InvoiceItem("bar", 100, vat=0.20, number=5)
        itemC = InvoiceItem("foo", 50, vat=0.10, number=2)
        a = Invoice("01.01.2006", None, [itemA, itemB, itemC])
        assert_equals(Decimal("620.666"), a.get_real_sum(netto=True))
        assert_equals(Decimal("620.67"), a.get_sum(netto=True))

    def test_summing_vat(self):
        """Test that all prices are summed correctly including the vat."""
        itemA = InvoiceItem("foo", 1.249, vat=0.10, number=2) # 2.7478
        itemB = InvoiceItem("bar", 1.5, vat=0.20, number=5) # 9
        itemC = InvoiceItem("foo", 5.0, vat=0.10, number=2) # 11
        a = Invoice("01.01.2006", None, [itemA, itemB, itemC])
        assert_equals(Decimal("22.7478"), a.get_real_sum())
        assert_equals(Decimal("22.75"), a.get_sum())

    def test_summing_rounding(self):
        """Test that netto sum + vat sums == brutto sum, even when rounding would give another sum."""
        itemA = InvoiceItem("foo", Decimal("0.803"), vat=Decimal("0.252801992528019925280199253"))
        # netto is 0.803
        # vat sum is 0.203
        # brutto is 1.006
        # customer should get sum of 1.00 unless get_real_sum is used 
        a = Invoice("", None, [itemA])
        assert_equals(Decimal("1.00"), a.get_sum(netto=False))
        assert_equals(Decimal("1.006"), a.get_real_sum(netto=False))

    def test_vat_sums(self):
        """Test that vat sums are correctly calculated."""
        itemA = InvoiceItem("a", 10, vat=0.20)
        itemB = InvoiceItem("b", 10, vat=0.10, number=10)
        itemC = InvoiceItem("c", 10, vat=0.20)
        itemD = InvoiceItem("d", 10, vat=0)
        a = Invoice("", None, [itemA, itemB, itemC, itemD])
        vats = a.get_vat_sums()
        assert_equals(3, len(vats))
        assert_equals((Decimal("0"), Decimal("0")), vats[0])
        assert_equals((Decimal("0.10"), Decimal("10")), vats[1])
        assert_equals((Decimal("0.20"), Decimal("4")), vats[2])

    def test_vat_sums_rounding(self):
        """Test that vat sums are correctly calculated (with and without limitation to two numbers after decimal point)."""
        itemA = InvoiceItem("a", 10.333, vat=0.20)
        a = Invoice("", None, [itemA])

        vats = a.get_real_vat_sums()
        assert_equals(1, len(vats))
        assert_equals((Decimal("0.2"), Decimal("2.0666")), vats[0])

        vats = a.get_vat_sums()
        assert_equals(1, len(vats))
        assert_equals((Decimal("0.2"), Decimal("2.07")), vats[0])

    def test_has_language(self):
        invoice = Invoice("", None)
        assert_equals(Invoice.DEFAULT_LANGUAGE, invoice.get_language())
        invoice = Invoice("", None, language="en")
        assert_equals("en", invoice.get_language())

    def test_has_currency(self):
        invoice = Invoice('', None)
        assert_equals('EUR', invoice.currency)
        invoice = Invoice('#', None, currency='USD')
        assert_equals('USD', invoice.currency)


if __name__ == "__main__":
    unittest.main()
